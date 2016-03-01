from lib.common_libs.plugin import Plugin

class Whois_command_Plugin(Plugin):
    """
    """

    _info = {
        "name"          : "Whois handler plugin",
        "shortname"     : "whois_command",
        "description"   : "This plugin responsible for all whois actions."
    }

    def __init__(self):
        Plugin.__init__(self)

    def initialize(self):
        """
        """
        self.connections_driver = self.loader.request_library("common_libs", "connections_driver")
        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("whois", self.work_with)
        self.channels = self.loader.request_library("common_libs", "channels")
        self.nicks = self.loader.request_plugin("nick_command")
        self.users = self.loader.request_plugin("user_command")

        self.formatter = self.loader.request_library("common_libs", "formatter")
        self.formatter.register_reply_code("RPL_WHOISUSER", "311")
        self.formatter.register_reply_code("RPL_WHOISSERVER", "312")
        self.formatter.register_reply_code("RPL_WHOISIDLE", "317")
        self.formatter.register_reply_code("RPL_ENDOFWHOIS", "318")
        self.formatter.register_reply_code("RPL_WHOISCHANNELS", "319")

    def work_with(self, message, connection):
        """
        """
        nickname = message.split(" ")[0]
        originator = connection.get_data("userline")
        self.log(2, "User '{userline}' requesting whois about '{nickname}'", {"userline": originator, "nickname": nickname})

        nickname_userline = self.nicks.get_nickname_data(nickname)["connection"].get_data("userline")

        data_about_user = self.users.get_user_data(nickname_userline)

        user_line = "{0} {1} {2} * {3}".format(nickname, data_about_user["username"], data_about_user["host"], data_about_user["realname"])
        channels_line = "{0} :{1}".format(nickname, " ".join(data_about_user["on_channels"]))
        server_line = "{0} localhost :Hardcoded server".format(nickname)

        data = []
        data.append(self.formatter.format_string("RPL_WHOISUSER", user_line, connection))
        data.append(self.formatter.format_string("RPL_WHOISCHANNELS", channels_line, connection))
        data.append(self.formatter.format_string("RPL_WHOISSERVER", server_line, connection))
        data.append(self.formatter.format_string("RPL_ENDOFWHOIS", ":End of /WHOIS list.", connection))

        return (0, data)
