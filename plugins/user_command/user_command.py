from lib.common_libs.plugin import Plugin

class User_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Users handler plugin",
        "shortname"     : "user_command",
        "description"   : "This plugin responsible for users holding."
    }

    def __init__(self):
        Plugin.__init__(self)
        self.__users = {}

    def add_channel(self, userline, channel):
        """
        """
        if userline in self.__users:
            if not channel in self.__users[userline]["on_channels"]:
                self.__users[userline]["on_channels"].append(channel)

    def add_user(self, message, connection):
        """
        """
        data = message.split()
        nickname = connection.get_data("nickname")
        host = connection.get_data("ptr")
        port = connection.get_data("port")
        hostport = "{0}:{1}".format(host, port)
        userline = "{0}!~{1}@{2}".format(nickname, data[0], host)
        if not userline in self.__users:
            self.__users[userline] = {}
            self.log(2, "User data: {data}", {"data": data})
            self.__users[userline]["nickname"] = nickname
            self.__users[userline]["username"] = data[0]
            self.__users[userline]["host"] = host
            self.__users[userline]["hostport"] = hostport
            self.__users[userline]["realname"] = " ".join(data[3:])
            self.__users[userline]["user_line"] = "{0}!~{1}@{2}".format(nickname, data[0], host)
            self.__users[userline]["on_channels"] = []
            connection.set_data("userline", userline)
            self.log(2, "Remembered user {nickname} as {userline}", {"nickname": data[0], "userline": self.__users[userline]["user_line"]})
            self.connections_driver.add_connection(userline, connection)
            return (0, "User: OK, got it! Remembered your connection from {0} as '{1}'".format(hostport, self.__users[userline]["user_line"]))
        else:
            return (1, "User: cannot remember you, because user with your host and port ({0}) already connected!".format(userline))

    def delete_user(self, userline):
        """
        """
        if userline in self.__users:
            self.log(2, "Deleting '{userline}' from connected users list...", {"userline": userline})
            del self.__users[userline]
        else:
            self.log(0, "{RED}ERROR:{RESET} connection '{CYAN}{userline}{RESET}' not found!", {"userline": userline})

    def get_user_data(self, userline):
        """
        """
        if userline in self.__users:
            return self.__users[userline]

    def initialize(self):
        """
        """
        self.log(1, "Initializing...")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("user", self.work_with)

        self.connections_driver = self.loader.request_library("common_libs", "connections_driver")

    def work_with(self, message, connection):
        """
        """
        self.log(2, "Received data: {data}", {"data": message})

        return self.add_user(message, connection)
