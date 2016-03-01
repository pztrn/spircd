from lib.common_libs.plugin import Plugin

class Ping_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Pings handler plugin",
        "shortname"     : "ping_command",
        "description"   : "This plugin responsible for channel ping-pong actions."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("ping", self.work_with)

    def work_with(self, message, connection):
        """
        """
        return (0, "PONG")
