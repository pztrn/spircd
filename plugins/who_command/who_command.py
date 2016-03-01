from lib.common_libs.plugin import Plugin

class Who_command_Plugin(Plugin):

    _info = {
        "name"          : "Who handler plugin",
        "shortname"     : "who_command",
        "description"   : "This plugin responsible for who requests holding."
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

        # Reply to /WHO command (<channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>)
        self.formatter.register_reply_code("RPL_ENDOFWHO", "315")
        self.formatter.register_reply_code("RPL_WHOREPLY", "352")
        self.formatter.register_reply_code("RPL_WHOSPCRPL", "354")

        self.commands_driver = self.loader.request_library("common_libs", "commands_driver")
        self.commands_driver.register_command("who", self.work_with)

    def who_on_channel(self, message, connection):
        """
        """
        channel = message
        channel_data = self.channels.get_channel_data(channel)
        if channel_data:
            users = []
            for item in channel_data["users"]:
                user_data = self.users.get_user_data(item)
                user = "{0} ~{1} {2} {3} {4} H :0 {5}".format(channel, user_data["username"], user_data["host"], "localhost", user_data["nickname"], user_data["realname"][1:])
                users.append(user)

            #users = "\r\n".join(users)

            # Compose final string.
            reply = ""
            for user in users:
                reply += self.formatter.format_string("RPL_WHOREPLY", user, connection)

            reply += self.formatter.format_string("RPL_ENDOFWHO", "{0} :End of /WHO list.\r\n".format(channel), connection)

            return (0, reply)
        else:
            return (1, "Channel {0} does not exists".format(channel))

    def work_with(self, message, connection):
        """
        """
        requester = connection.get_data("userline")

        if message.startswith("#"):
            self.log(2, "User {userline} requested users list for channel {channel}", {"userline": requester, "channel": message})
            return self.who_on_channel(message, connection)

        return (0, "WHO: Command not supported")
