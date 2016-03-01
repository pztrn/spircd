from lib.common_libs.plugin import Plugin

class Nick_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Nicknames handler plugin",
        "shortname"     : "nick_command",
        "description"   : "This plugin responsible for nicknames holding."
    }

    def __init__(self):
        Plugin.__init__(self)
        self.__nicknames = {}

    def add_nickname(self, message, connection):
        """
        """
        nickname = message.split(" ")[0]
        if not nickname in self.__nicknames:
            self.log(2, "Adding '{nickname}' to connected nicknames list...", {"nickname": message})
            self.__nicknames[nickname] = {
                "nickname": nickname,
                "connection": connection
            }
            connection.set_data("nickname", message)
            return (0, "OK")
        else:
            self.log(1, "Nickname '{BLUE}{nickname}{RESET}' already connected!", {"nickname": nickname})
            return (1, "Nickname already present")

    def delete_nickname(self, nickname):
        """
        """
        if nickname in self.__nicknames:
            self.log(2, "Deleting '{nickname}' from connected nicknames list...", {"nickname": nickname})
            del self.__nicknames[nickname]
        else:
            self.log(0, "{RED}ERROR:{RESET} connection '{CYAN}{nickname}{RESET}' not found!", {"nickname": nickname})

    def get_nickname_data(self, nickname):
        """
        """
        if nickname in self.__nicknames:
            return self.__nicknames[nickname]
        else:
            return None

    def initialize(self):
        """
        """
        self.log(1, "Initializing...")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("nick", self.work_with)

    def work_with(self, message, connection):
        """
        """
        self.log(2, "Received data: {data}", {"data": message})

        retcode, data = self.add_nickname(message, connection)

        if not retcode:
            return (0, None)
        else:
            return (1, "Nickname: this nickname already present as online on server. Please, choose another nickname!")
