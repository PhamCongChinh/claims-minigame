import os
import sys
import time
from colorama import *
import json
import random
import cloudscraper
scraper = cloudscraper.create_scraper()

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")

class Tomarket:
    def __init__(self):
        pass
    def headers(self):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Origin": "https://mini-app.tomarket.ai",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://mini-app.tomarket.ai/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

    def login(self, data):
        url = f"https://api-web.tomarket.ai/tomarket-game/v1/user/login"
        headers = self.headers()
        payload = {
            "init_data": data,
            "invite_code": "",
        }
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def balance(self, token):
        url = f"https://api-web.tomarket.ai/tomarket-game/v1/user/balance"
        headers = self.headers()
        headers["Authorization"] = token
        response = scraper.post(url=url, headers=headers)
        return response

    def claim_game(self, token, point):
        url = f"https://api-web.tomarket.ai/tomarket-game/v1/daily/claim"
        headers = self.headers()
        headers["Authorization"] = token
        payload = {
            "game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07",
            "point": point
        }
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def main(self):
        while True:
            # Login
            data = open(data_file, "r").read().splitlines()
            try:
                login = self.login(data=data[0]).json()
                token = login["data"]["access_token"]
                if token:
                    balance = self.balance(token).json()
                    print(balance["data"]["available_balance"])

                    point = random.randint(500, 600)
                    claim_game = self.claim_game(token, point)
                    print(claim_game)
                    print("Finish!")
            except Exception as e:
                print(f"Get auth data error!!!", e)
            print()
            wait_time = 15 * 60
            time.sleep(wait_time)
if __name__ == "__main__":
    try:
        tomarket = Tomarket()
        tomarket.main()
    except KeyboardInterrupt:
        sys.exit()