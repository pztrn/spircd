from lib.common_libs.plugin import Plugin

class Names_command_Plugin(Plugin):

    _info = {
        "name"          : "Names handler plugin",
        "shortname"     : "names_command",
        "description"   : "This plugin responsible for names requests holding."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.channels = self.loader.request_library("common_libs", "channels")
        self.formatter = self.loader.request_library("common_libs", "formatter")
        self.nicks = self.loader.request_plugin("nick_command")
        self.users = self.loader.request_plugin("user_command")

        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("names", self.work_with)

        self.formatter.register_reply_code("RPL_NAMREPLY", "353")
        self.formatter.register_reply_code("RPL_ENDOFNAMES", "366")

    def names_on_channel(self, channel, connection):
        """
        """
        self.log(2, "Obtaining NAMES for channel {channel}...", {"channel": channel})
        channel_data = self.channels.get_channel_data(channel)
        nicks = []
        for item in channel_data["users"]:
            user_data = self.users.get_user_data(item)
            nicks.append(user_data["nickname"])

        nicks = " ".join(nicks)
        reply = ""
        reply += self.formatter.format_string("RPL_NAMREPLY", "= {0} :{1}\r\n".format(channel, nicks), connection)
        reply += self.formatter.format_string("RPL_ENDOFNAMES", "{0} :End of /NAMES list.\r\n".format(channel), connection)

        return (0, reply)

    def work_with(self, message, connection):
        """
        """
        self.log(2, "Received data: {data}", {"data": message})
        if message.startswith("#"):
            return self.names_on_channel(message)

