from lib.common_libs.plugin import Plugin

class Join_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Joins handler plugin",
        "shortname"     : "join_command",
        "description"   : "This plugin responsible for channel join actions."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.channels = self.loader.request_library("common_libs", "channels")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("join", self.work_with)
        self.connections_driver = self.loader.request_library("common_libs", "connections_driver")
        self.names_plugin = self.loader.request_plugin("names_command")
        self.users = self.loader.request_plugin("user_command")
        self.who_plugin = self.loader.request_plugin("who_command")

    def work_with(self, message, connection):
        """
        """
        self.log(2, "Received data: {data}", {"data": message})
        self.log(2, "User {nickname} joins channel {channel}", {"nickname": connection.get_data("nickname"), "channel": message})

        retcode, status = self.channels.join_channel(connection, message)
        if retcode == 0:
            # Send everyone else a message about joining.
            channel_data = self.channels.get_channel_data(message)
            if channel_data:
                send_to_users = []
                for user in channel_data["users"]:
                    if user == connection.get_data("userline"):
                        continue

                    send_to_users.append(user)

                message_to_others = ":{0} JOIN {1}".format(connection.get_data("userline"), message)
                for user in send_to_users:
                    self.connections_driver.send_message(user, message_to_others)

            # Add channel to user's list.
            self.users.add_channel(connection.get_data("userline"), message)

            who_on_channel = self.who_plugin.who_on_channel(message, connection)
            names_on_channel = self.names_plugin.names_on_channel(message, connection)

            data = []
            data.append(status)
            data.append(who_on_channel[1])
            data.append(names_on_channel[1])

            return (0, "\r\n".join(data))
        else:
            return (1, status)
