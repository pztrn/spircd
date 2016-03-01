from lib.common_libs.plugin import Plugin

class Privmsg_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Messages handler plugin",
        "shortname"     : "privmsg_command",
        "description"   : "This plugin responsible for all messaging actions."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.connections_driver = self.loader.request_library("common_libs", "connections_driver")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("privmsg", self.work_with)
        self.channels = self.loader.request_library("common_libs", "channels")
        self.nicks = self.loader.request_plugin("nick_command")

    def send_to_user(self, userline, destination, message):
        """
        """
        nickname_data = self.nicks.get_nickname_data(destination)
        message = ":{0} PRIVMSG {1} :{2}".format(userline, destination, message)
        self.connections_driver.send_message(nickname_data["connection"].get_data("userline"), message)

    def work_with(self, message, connection):
        """
        """
        data = message.split()
        destination = data[0]
        message = " ".join(data[1:])
        # Remove ":" from the beginning of message.
        message = message[1:]
        self.log(2, "New message to {destination}: {message}", {"destination": destination, "message": message})

        if destination.startswith("#"):
            self.channels.send_message(connection.get_data("userline"), destination, message)
        else:
            self.send_to_user(connection.get_data("userline"), destination, message)

        return (0, None)
