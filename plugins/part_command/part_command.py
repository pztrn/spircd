from lib.common_libs.plugin import Plugin

class Part_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Part handler plugin",
        "shortname"     : "part_command",
        "description"   : "This plugin responsible for channel part actions."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.channels = self.loader.request_library("common_libs", "channels")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("part", self.work_with)
        self.connections_driver = self.loader.request_library("common_libs", "connections_driver")

    def work_with(self, message, connection):
        """
        """
        nickname = connection.get_data("nickname")
        userline = connection.get_data("userline")

        retcode, status = self.channels.leave_channel(message, connection)

        channel_data = self.channels.get_channel_data(message.split(" ")[0])

        send_to_users = []
        for item in channel_data["users"]:
            if userline == channel_data["users"]:
                continue

            send_to_users.append(item)

        for user in send_to_users:
            self.connections_driver.send_message(user, status)

        return (0, status)
