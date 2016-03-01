from lib.common_libs.library import Library

"""@package commands_parser
This package contains class that is needed for parsing received messages.
"""

class Commands_parser(Library):
    """
    This class responsible for complete process of working with received
    messages.

    It will get commands from messages and launch approriate plugins.
    """
    def __init__(self):
        Library.__init__(self)

    def init_library(self):
        """
        Library initialization.
        """
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")

    def parse_command(self, connection):
        """
        This method responsible for executing plugins for commands.

        It will obtain a list of messages from connection instance,
        iterate thru them and launch approriate plugins.

        While iterating thru list of messages it will obtain
        command and its parameters and launch approriate plugin.
        E.g., for message "NICK nickname" it will launch
        plugins.nick.Nick_Plugin.work_with() (thru commands_driver)
        and pass "nickname" and pointer to connection to it.

        @param connection Instance of Irc()
        @retval data_to_push_back List of strings to send back to
        client.
        """
        # List of strings.
        data_to_push_back = []

        commands = connection.get_data("message")
        self.log(2, commands)

        for line in commands:
            if len(line) > 0:
                # Get actual command.
                command = line.split()[0]
                # Get parameters to command.
                line_data = " ".join(line.split()[1:])
                self.log(2, "Trying to obtain plugin for command '{BLUE}{command}{RESET}'...", {"command": command})
                # Check if requested command is registered on server.
                # Error will be sent back if command wasn't registered.
                command_plugin = self.commands_driver.check_command(command)
                if command_plugin:
                    # Send command, message and pointer to connection to
                    # Commands_driver() instance, which will take care about
                    # launching approriate plugin. We will wait for two parameters -
                    # return code and data. If return code == 0, then everything
                    # is okay. Any other return code means error, that later
                    # will be projected to IRC error code.
                    retcode, data = self.commands_driver.try_command(command, line_data, connection)
                    if retcode == 0:
                        if type(data) == list:
                            data_to_push_back += data
                        else:
                            data_to_push_back.append(data)
                    else:
                        # Probably, we might do something interesting here.
                        # This data is an error.
                        data_to_push_back.append(data)
                else:
                    # Push back a message about missing command. It will appear
                    # in console tab in client.
                    self.log(0, "{RED}ERROR:{RESET} no plugin found for command '{BLUE}{command}{RESET}'...", {"command": command})
                    data_to_push_back.append("{0}: No such command".format(command))

        return data_to_push_back

    def prepare(self, data):
        """
        This method will prepare collected data to be sent back to
        client.

        Eventually it will create a string, where strings will
        be delimited with "\r\n" (IRC RFC line-break thing).

        @param data String or list of strings to compile into one
        string.
        @retval string Compiled string of strings.
        """
        # If we got string - split it into list first.
        if type(data) == str:
            if "\r\n" in data:
                # If string was already formatted with "\r\n".
                data = data.split("\r\n")
            else:
                # If string is using "\n" instead of "\r\n".
                data = data.split("\n")
        # If we already having list here - just iterate thru it and
        # make sure that strings here are okay.
        elif type(data) == list:
            new_data = []
            for item in data:
                if item:
                    if "\r\n" in item:
                        # If we got a string with "\r\n" in list - split
                        # it into another list and append to normalized
                        # one.
                        item = item.split("\r\n")

                        # Append to normalized list.
                        new_data = new_data + item
                    else:
                        new_data.append(item)

            # Normalized list replaces not-normalized one.
            data = new_data

        # Clean up the list.
        # Make a copy of it we will iterate thru.
        old_data = data.copy()
        for item in old_data:
            index = data.index(item)
            # Remove NoneType's that can be in list if command was successful.
            if not item:
                data.pop(index)

        # Do not send empty lines.
        if len(data) == 0:
            return "NOTHING_TO_SEND"

        # Join list into one string with "\r\n" as delimiter.
        data = "\r\n".join(data)
        # Add final "\r\n", so client will know that data flow ends here.
        data = data + "\r\n"
        return data
