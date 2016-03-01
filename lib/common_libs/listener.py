import asyncio

from lib.common_libs.library import Library
from lib.protocols.irc import Irc

"""@package Listener
This package contains class which will start listening for client
connections in asyncio loop.
"""

class Listener(Library):
    """
    This class responsible for starting listening for client connections
    in asyncio loop.
    """

    def __init__(self):
        Library.__init__(self)

    def init_library(self):
        """
        Library initialization.

        For this class doing nothing that just print initialization
        message.
        """
        self.log(0, "Initializing TCP Listener...")

    def start_listening(self):
        """
        This method starts listening on port.
        """
        loop = asyncio.get_event_loop()
        coro = loop.create_server(Irc, "localhost", 6667)
        self.log(0, "Starting listening for connections on tcp://localhost:6667/")
        server = loop.run_until_complete(coro)
        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print()
            self.close_app()
        except RuntimeError as e:
            self.log(0, "{RED}ERROR:{RESET} RuntimeError appeared: {error}", {"error": e})
            self.log(0, "{RED}Error appeared in __listen_to_tcp() method.{RESET}")

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
