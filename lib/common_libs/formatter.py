from lib.common_libs.library import Library

"""@package formatter
This package contains class that responsible for formatting messages
before they will be sent back to client.
"""

class Formatter(Library):
    """
    This class responsible for formatting messages before they will be
    sent to client.
    """

    def __init__(self):
        Library.__init__(self)

        self.__reply_codes = {}

    def format_string(self, reply_code_str, string, connection):
        """
        Formats string for sending back to client.

        Generic IRC message have this format:

            :hostname_of_server reply_code client_nickname message
        """
        data = {
            "host"      : "localhost",
            "nickname"  : connection.get_data("nickname"),
            "reply_code": self.__get_reply_code(reply_code_str),
        }

        if not string.endswith("\r\n"):
            string += "\r\n"

        data["string"] = string

        string = ":{host} {reply_code} {nickname} {string}".format(**data)
        return string

    def register_reply_code(self, string, integer):
        """
        This method registering reply code.

        Registration of reply code makes message formatting process
        easier and plugins source code cleaner, because developer
        will not use numeric value, but it's representation in
        string. This also helps make source code more readable :).

        Most of reply codes can be found here:
        https://www.alien.net.au/irc/irc2numerics.html

        @param string String representation of reply code.
        @param integer Numeric representation of reply code.
        """
        if not string in self.__reply_codes:
            self.log(2, "Registered reply code: {reply_code_str} => {reply_code_int}", {"reply_code_str": string, "reply_code_int": integer})
            self.__reply_codes[string] = integer

    def __get_reply_code(self, reply_code_str):
        """
        This method returns numeric representation of reply code.
        Used only internally.

        Reason why this module even exists - is to use simple
        method call while forming dictionary for string formatting.
        If plugin developer forgot to register it - it will return
        None, instead of crashing whole process.

        @param reply_code_str String representation of reply code.
        """
        if reply_code_str in self.__reply_codes:
            return self.__reply_codes[reply_code_str]
