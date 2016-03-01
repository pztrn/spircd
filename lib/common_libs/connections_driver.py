from lib.common_libs.library import Library

"""@package connections_driver
This package contains class that responsible for sending messages to
clients.

It is only used when there is a need to send message from one client
to another.
"""

class Connections_driver(Library):
    """
    This class that responsible for sending messages to
    clients.

    It is only used when there is a need to send message from one client
    to another.
    """
    def __init__(self):
        Library.__init__(self)

        self.__connections = {}

    def add_connection(self, userline, connection):
        """
        This method adds connection pointer to internal dictionary for
        later usage.

        All connections here are tagged with userline.

        @param userline User line for connection.
        @param connection Instance of Irc()
        """
        if not userline in self.__connections:
            self.log(2, "Adding connection for {BLUE}{userline}{RESET} to list of active connections...", {"userline": userline})
            self.__connections[userline] = connection
        else:
            self.log(0, "{RED}ERROR:{RESET} connection for {BLUE}{userline}{RESET} already exist!", {"userline": userline})

    def init_library(self):
        """
        Library initialization.
        """
        self.commands_parser = self.loader.request_library("common_libs", "commands_parser")

    def send_message(self, userline, message):
        """
        This method sends message to client.

        It is used when one client want to send message to another client.
        For example, see plugins.privmsg.Privmsg_Plugin.work_with() method.

        @param userline User line of client we will send message to.
        @param message Message we will send.
        """
        self.log(2, "Sending to {userline}: '{message}'", {"userline": userline, "message": message})
        writer = self.__connections[userline].get_transport()
        writer.write(self.commands_parser.prepare(message).encode())
