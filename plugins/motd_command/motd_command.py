from lib.common_libs.plugin import Plugin

class Motd_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "MOTD handler plugin",
        "shortname"     : "motd_command",
        "description"   : "This plugin responsible for all MOTD actions."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("motd", self.work_with)

    def work_with(self, message, connection):
        """
        """
        self.log(2, "Received data: {data}", {"data": message})
        return (0, "MOTD")
