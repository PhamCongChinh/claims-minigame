from datetime import datetime
import os
import sys
import json

from colorama import Fore, Style

class Common:
    def __init__(self):
        self.red = Fore.LIGHTRED_EX
        self.yellow = Fore.LIGHTYELLOW_EX
        self.green = Fore.LIGHTGREEN_EX
        self.black = Fore.LIGHTBLACK_EX
        self.blue = Fore.LIGHTBLUE_EX
        self.white = Fore.LIGHTWHITE_EX
        self.reset = Style.RESET_ALL

    def file_path(self, file_name: str):
        caller_dir = os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename))
        file_path = os.path.join(caller_dir, file_name)
        return file_path

    def create_line(self, length: int):
        line = self.white + "-" * length
        return line

    def create_banner(self, game_name: str):
        banner = f"""
            {self.blue}Play {self.white}{game_name}
        """
        return banner

    # Terminal
    def clear_terminal(self):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{self.black}[{now}]{self.reset} {msg}{self.reset}")

    # Config
    def get_config(self, config_file: str, config_name: str):
        config_status = (
                json.load(open(config_file, "r")).get(config_name, "false").lower() == "true"
        )
        return config_status
common = Common()