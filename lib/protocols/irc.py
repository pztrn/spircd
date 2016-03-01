import asyncio

from lib.common_libs import common
from lib.common_libs.library import Library

"""@package Irc
This is IRC protocol handler, which will take care about data flowing
for IRC protocol. Every connection is an instance of Irc() class,
which contains everything about connection - IP address, PTR, port,
socket writer, username, nickname and so on.
"""

class Irc(Library, asyncio.Protocol):
    """
    This class responsible for IRC protocol. Every connection is an
    instance of this class.

    This class also capable to store connection information, like
    IP address, port, nickname, userline, and so on.
    """

    def __init__(self):
        Library.__init__(self)
        asyncio.Protocol.__init__(self)

        # Connection-related data.
        self.__data = {}

        self.__just_connected = 1

    def connection_lost(self, exc):
        """
        This method executes when connection was closed or timed out.

        @param exc Exception with connection termination description.
        """
        self.log(0, "Connection lost: {error_text}. User: {user}, address: {hostport}", {"error_text": exc, "user": "test", "hostport": self.__data["hostport"]})

    def connection_made(self, transport):
        """
        This method executes when connection is created.

        @param transport Transport for connection.
        """
        # Getting Loader() instance.
        self.loader = common.LOADER
        # Getting logger :)
        self.log = self.loader.request_library("common_libs", "logger").log
        # Configuration.
        self.config = self.loader.request_library("common_libs", "config")
        # IRC commands parser.
        self.commands_parser = self.loader.request_library("common_libs", "commands_parser")
        # DNS querier.
        self.dns_querier = self.loader.request_library("common_libs", "dns_querier")
        self.nicknames = self.loader.request_plugin("nick_command")
        self.usernames = self.loader.request_plugin("user_command")
        # Peer information (host, port).
        peer = transport.get_extra_info('peername')
        # Set some data about this connection.
        self.__data["hostport"] = str(peer[0]) + ":" + str(peer[1])
        self.set_data("host", peer[0])
        self.set_data("port", peer[1])
        # Inform user that we are about to getting his hostname.
        transport.write(self.commands_parser.prepare("NOTICE AUTH :*** Looking for your hostname...").encode())
        # Perform a DNS query.
        ptr = self.dns_querier.get_ptr(self.get_data("host"))
        # If PTR was found - use it. Otherwise fall back to IP address.
        if ptr:
            self.set_data("ptr", ptr)
            transport.write(self.commands_parser.prepare("NOTICE AUTH :*** Found your hostname: {0}".format(ptr)).encode())
        else:
            self.set_data("ptr", peer[0])
            transport.write(self.commands_parser.prepare("NOTICE AUTH :*** Hostname not found, using your IP...").encode())

        self.log(1, "Connection from {}".format(self.__data["hostport"]))

        # Make transport be available within this class.
        self.transport = transport

    def data_received(self, data):
        """
        This method executes when data was received.

        It also executes some preliminary message parsing, like splitting
        message into list for later processing by Commands_parser(), getting
        PTR records for connection, and so on.

        It also have hardcoded QUIT message action, which will close
        connection, if client send this message. Connection will be closed
        right after QUIT IRC command will perform actions.

        @param data Bytes of received data.
        """
        message = data.decode()
        self.log(2, "Data received: {0}".format(message))

        # Set connection state.
        # On first data receiving it will be "new_connection", so
        # MOTD, capabilities and so on can be sent to client.
        # On second data receiving connection state will be put to
        # "connected", which means that preliminary data was
        # already sent to client.
        if self.__just_connected:
            self.set_data("status", "new_connection")
            self.__just_connected = 0
        else:
            self.set_data("status", "connected")

        # Make message attribute be a list of strings.
        self.set_data("message", message.split("\r\n"))

        self.log(2, "Connection status: {connstatus}, message: {message}", {"connstatus": self.get_data("status"), "message": self.get_data("message")})

        data = self.commands_parser.parse_command(self)

        if self.get_data("status") == "new_connection":

            # Standard hello strings.
            self.transport.write(self.commands_parser.prepare(":localhost 001 {0} :Hello, {0}, and welcome to {1}!".format(self.get_data("nickname"), self.config.get_temp_value("main/network_name"))).encode())
            self.transport.write(self.commands_parser.prepare(":localhost 002 {2} :Your host is {0}, running spircd version {1}".format("localhost", "0.1", self.get_data("nickname"))).encode())
            # These lines should be dynamically generated, in future.
            self.transport.write(self.commands_parser.prepare(":localhost 005 {0} MAXCHANNELS=20 MAXBANS=45 NICKLEN=15 :are supported by this server").format(self.get_data("nickname")).encode())
            self.transport.write(self.commands_parser.prepare(":localhost 005 {0} MAXNICKLEN=15 TOPICLEN=250 AWAYLEN=160 KICKLEN=250 CHANNELLEN=200 MAXCHANNELLEN=200 CHANTYPES=#& PREFIX=(ov)@+ STATUSMSG=@+ CHANMODES=b,k,l,imnpstrDducCNMT CASEMAPPING=rfc1459 NETWORK=TESTNET :are supported by this server").format(self.get_data("nickname")).encode())

        data = self.commands_parser.prepare(data)
        # Send reply, only if there is something to send.
        if data != "NOTHING_TO_SEND":
            self.transport.write(data.encode())

        # If "QUIT" was found in received message - force transport
        # shutdown.
        if "QUIT" in message:
            self.transport.close()

    def eof_received(self):
        """
        """
        pass

    def get_data(self, key):
        """
        This method returns connection-related data to caller.

        @param key Key to return
        @retval value Value for key.
        """
        if key in self.__data:
            return self.__data[key]
        else:
            return None

    def get_data_keys(self):
        """
        This method returns keys for all connection-related data.

        @retval list-of-keys List of keys for connection-related data.
        """
        return self.__data.keys()

    def get_transport(self):
        """
        This method returns pointer to transport for sending data to
        client. Usually should only be used by Connections_driver() class.

        @retval transport Pointer to this connection's transport.
        """
        return self.transport

    def set_data(self, key, value):
        """
        This method sets connection-related data.

        Data can be set from this class, libraries or plugins (e.g.
        nickname changes).

        @param key Key to be set.
        @param value Value for key.
        """
        self.log(2, "For connection from '{CYAN}{hostport}{RESET}' data was set: {YELLOW}{key}{RESET} => {BLUE}{value}{RESET}", {"hostport": self.__data["hostport"], "key": key, "value": value})
        self.__data[key] = value
