from lib.common_libs.plugin import Plugin

class Mode_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Mode plugin",
        "shortname"     : "mode_command",
        "description"   : "This plugin responsible for modes holding."
    }

    def __init__(self):
        Plugin.__init__(self)

        self.__umodes = {}
        self.__chanmodes = {}

    def initialize(self):
        """
        """
        self.users = self.loader.request_plugin("user_command")
        self.nicks = self.loader.request_plugin("nick_command")
        self.formatter = self.loader.request_library("common_libs", "formatter")

        self.formatter.register_reply_code("RPL_UMODEIS", "221")

        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("mode", self.work_with)

    def work_with(self, message, connection):
        """
        """
        self.log(2, "Received data: {data}", {"data": message})
        return (0, None)
