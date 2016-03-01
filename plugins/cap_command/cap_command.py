from lib.common_libs.plugin import Plugin

class Cap_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Capabilities plugin",
        "shortname"     : "cap_command",
        "description"   : "This plugin responsible for capabilities holding."
    }

    def __init__(self):
        Plugin.__init__(self)
        self.__capabilities = []

    def add_capability(self, capability_name):
        """
        """
        if not capability_name in self.__capabilities:
            self.capabilities.append(capability_name)

    def get_capabilities_string(self):
        """
        """
        return " ".join(self.__capabilities)

    def initialize(self):
        """
        """
        self.log(1, "Initializing...")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("cap", self.work_with)

    def work_with(self, message, connection):
        """
        """
        self.log(2, "Received data: {data}", {"data": message})

        if message in ("LS", "LIST"):
            # We does not support capabilities yet.
            return (0, None)
        else:
            return (1, "Invalid capabilities command: {0}".format(message))
