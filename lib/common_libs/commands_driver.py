import sys

from lib.common_libs.library import Library

"""@package commands_driver
This package contains class that responsible for rounting messages to
plugins.
"""

class Commands_driver(Library):
    """
    This class responsible for holding methods pointers that responsible
    for commands, as well as launching them.
    """

    def __init__(self):
        Library.__init__(self)

        self.__commands = {}

        self.__supported_chanmodes = []
        self.__supported_umodes = []

    def check_command(self, command):
        """
        Check if requested command exists.

        @param command Command name without slashes.
        @retval int Integer that represents presence. 1 - present,
        0 - not present.
        """
        command_module_name = "{0}_command".format(command)
        if command_module_name.lower() in self.__commands:
            return 1

    def try_command(self, command, parameters, connection):
        """
        Tries to execute command and return it's result to caller.

        @param command Command to execute.
        @retval string Command's reply.
        """
        command_module_name = "{0}_command".format(command)
        if command_module_name.lower() in self.__commands:
            return self.__commands[command_module_name.lower()]["method"](parameters, connection)

    def register_command(self, command, method):
        """
        Registers command.

        @param command command name without slashes.
        @param method pointer to function which is responsible for command.
        """
        caller = sys._getframe(1).f_locals["self"].__class__.__name__
        command_module_name = "{0}_command".format(command)
        if not command_module_name.lower() in self.__commands:
            self.__commands[command_module_name.lower()] = {
                "name"          : command_module_name.lower(),
                "method"        : method
            }
            self.log(1, "Registered command {YELLOW}{command}{RESET} from {MAGENTA}{caller}{RESET}", {"command": command, "caller": caller})
        else:
            self.log(0, "Command {command} already registered!", {"command": command})
            return 1

