#!/usr/bin/env python3

import json
import os
import sys

# Load Regius.
system_regius = 0
try:
    from regius.regius import Regius
    system_regius = 1
except:
    pass

if not system_regius:
    if os.path.exists("config.json"):
        preseed = json.loads(open("config.json", "r").read())
        if "paths" in preseed and "regius" in preseed["paths"]:
            sys.path.insert(0, preseed["paths"]["regius"])

            import regius

class SPIrcD:
    def __init__(self, regius_instance):
        self.__regius = regius_instance
        self.loader = self.__regius.get_loader()
        self.config = self.loader.request_library("common_libs", "config")

        # ToDo: make it configurable!
        self.config.set_temp_value("main/network_name", "pztrn's Test IRC Network")

        self.log = self.loader.request_library("common_libs", "logger").log
        self.log(0, "Framework initialization complete.")

        self.__load_plugins()

        self.listener = self.loader.request_library("common_libs", "listener")
        self.listener.start_listening()

    def __load_plugins(self):
        """
        """
        self.log(0, "Loading plugins...")
        for plugin in os.listdir(os.path.join(self.config.get_temp_value("SCRIPT_PATH"), "plugins")):
            self.log(1, "Loading plugin '{CYAN}{plugin_name}{RESET}'...", {"plugin_name": plugin})
            self.loader.request_plugin(plugin)

if __name__ == "__main__":
    print("Starting SPIrcD...")
    # Making application path be available to Regius, and also
    # put it into beginning of sys.path, so plugins, UIs and
    # libraries will be loaded from here first.
    # Also, Logger() will also take sys.path[0] for placing logs.
    app_path = os.path.abspath(__file__).split(os.path.sep)[:-1]
    app_path = os.path.sep.join(app_path)

    regius = regius.init(preseed, app_path)
    exit(SPIrcD(regius))
