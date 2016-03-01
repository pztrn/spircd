from lib.common_libs.library import Library

class Channels(Library):
    def __init__(self):
        Library.__init__(self)

        self.__channels = {}

    def add_channel(self, channel_name):
        """
        """
        if not channel_name in self.__channels:
            self.__channels[channel_name] = {
                "users": [],
                "history": [],
                "access": {}
            }
            return (0, None)
        else:
            return (1, "Cannot create channel {0}: already created.".format(channel_name))

    def get_channel_data(self, channel):
        """
        """
        if channel in self.__channels:
            return self.__channels[channel]

    def init_library(self):
        """
        """
        self.nicks = self.loader.request_plugin("nick_command")
        self.users = self.loader.request_plugin("user_command")
        self.connections_driver = self.loader.request_library("common_libs", "connections_driver")

    def join_channel(self, connection, channel):
        """
        """
        # Verify that channel name begins with "#".
        if not channel.startswith("#"):
            return (1, "Invalid channel name. Channels names should begins with '#'!")

        nickname = connection.get_data("nickname")
        userline = connection.get_data("userline")
        self.log(2, "User {nickname} joins channel {channel_name}", {"nickname": userline, "channel_name": channel})

        if not channel in self.__channels:
            self.add_channel(channel)

        if not connection.get_data("userline") in self.__channels[channel]["users"]:
            self.__channels[channel]["users"].append(connection.get_data("userline"))

        return (0, ":{0} JOIN :{1}".format(userline, channel))

    def leave_channel(self, message, connection):
        """
        """
        channel = message.split(" ")[0]
        part_message = message.split(" ")[1]
        # Verify that channel name begins with "#".
        if not channel.startswith("#"):
            return (1, "Invalid channel name. Channels names should begins with '#'!")

        nickname = connection.get_data("nickname")
        userline = connection.get_data("userline")

        idx = self.__channels[channel]["users"].index(userline)
        if idx:
            self.__channels[channel]["users"].pop(idx)

        return (0, ":{0} PART {1} {2}".format(userline, channel, part_message))

    def send_message(self, userline, channel, message):
        """
        """
        self.log(2, "Message from {userline} to channel {channel} >>> {message}", {"userline": userline, "channel": channel, "message": message})

        # Composing list of users we will send message to.
        send_to_users = []

        for channel_userline in self.__channels[channel]["users"]:
            if channel_userline == userline:
                continue

            send_to_users.append(channel_userline)

        # Compose message.
        message = ":{0} PRIVMSG {1} :{2}".format(userline, channel, message)

        # Send message to users.
        if len(send_to_users) > 0:
            for user in send_to_users:
                self.connections_driver.send_message(user, message)
        else:
            self.log(2, "Only one user in channel, will not send anything to anyone")
