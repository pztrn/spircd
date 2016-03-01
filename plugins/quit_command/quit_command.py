from lib.common_libs.plugin import Plugin

class Quit_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Quit plugin",
        "shortname"     : "quit_command",
        "description"   : "This plugin responsible for quit handling."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.__nicks = self.loader.request_plugin("nick_command")
        self.__users = self.loader.request_plugin("user_command")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("quit", self.work_with)

    def work_with(self, message, connection):
        """
        """
        self.__nicks.delete_nickname(connection.get_data("nickname"))
        self.__users.delete_user(connection.get_data("userline"))
        self.log(2, "Received QUIT for '{userline}'", {"userline": connection.get_data("userline")})

        return (0, "QUIT: Ok")
