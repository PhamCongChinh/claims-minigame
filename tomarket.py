import os
import sys
import time
from datetime import datetime

from colorama import *
import json
import random
import cloudscraper

from base import common, countdown

scraper = cloudscraper.create_scraper()
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
# Construct the full paths to the files
data_file = os.path.join(script_dir, "data/tomarket.txt")

class Tomarket:
    def __init__(self):
        self.banner = common.create_banner(game_name="Tomarket")
        self.line = common.create_line(length=45)
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
            "from": "",
            "init_data": data,
            "invite_code": ""
        }
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def get_balance(self, token):
        url = f"https://api-web.tomarket.ai/tomarket-game/v1/user/balance"
        headers = self.headers()
        headers["Authorization"] = token
        response = scraper.post(url=url, headers=headers)
        return response

    def start_farming(self, token):
        url = f"https://api-web.tomarket.ai/tomarket-game/v1/farm/start"
        headers = self.headers()
        headers["Authorization"] = token
        payload = {
            "game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"
        }
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"

        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def check_in_daily(self, token):
        url = f"https://api-web.tomarket.ai/tomarket-game/v1/daily/claim"
        headers = self.headers()
        headers["Authorization"] = token
        payload = { "game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07" }
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def start_game(self, token):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/game/play"
        headers = self.headers()
        headers["Authorization"] = token
        payload = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"}
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def claim_game(self, token, point):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/game/claim"
        headers = self.headers()
        headers["Authorization"] = token
        payload = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d", "points": point}
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def end_farming(self, token):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/farm/claim"
        headers = self.headers()
        headers["Authorization"] = token
        payload = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
        data = json.dumps(payload)
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def main(self):
        while True:
            common.clear_terminal()
            print(self.banner)
            # Login
            data = open(data_file, "r").read().splitlines()
            number_account = len(data)
            end_at_list = []
            common.log(f"Số lượng tài khoản: {number_account}")
            for no, data in enumerate(data):
                try:
                    login = self.login(data=data).json()
                    token = login["data"]["access_token"]
                    if token:
                        user_info = self.get_balance(token).json().get("data")
                        available_balance = user_info["available_balance"]
                        play_passes = user_info["play_passes"]
                        current_time = user_info["timestamp"]
                        common.log(f"{common.green}Số dư sẵn có: {common.yellow}{available_balance} cà chua")

                        check_in_daily = self.check_in_daily(token).json()
                        if check_in_daily["status"] == 200:
                            common.log(f"{common.green}Check in thành công!")
                        else:
                            common.log(f"{common.red}Đã check in rồi!")

                        if 'farming' not in user_info.keys():
                            start_farming = self.start_farming(token)
                            if start_farming.status_code == 200:
                                common.log(f"{common.yellow}Hái thành công")
                                user_info = self.get_balance(token).json().get("data")
                            else:
                                common.log(f"{common.red}Hái lỗi rồi")

                        end_farming_time = user_info["farming"]["end_at"]
                        if current_time > end_farming_time:
                            end_farming = self.end_farming(token)
                            if end_farming.status_code == 200:
                                common.log(f"{common.yellow} Bắt đầu hái thành công")
                                user_info = self.get_balance(token).json().get("data")
                                end_farming_time = user_info["farming"]["end_at"]
                            else:
                                common.log(f"{common.yellow}Kết thúc hái lỗi")
                        else:
                            common.log(f"{common.yellow}Chưa đến thời gian hái")

                        readable_time = datetime.fromtimestamp(end_farming_time).strftime("%Y-%m-%d %H:%M:%S")
                        common.log(f"{common.green}Hái kết thúc lúc: {readable_time}")
                        end_at_list.append(end_farming_time)

                        # Play game
                        available_tickets = user_info["play_passes"]
                        if available_tickets > 0:
                            common.log(f"{common.green}Số dư game: {common.yellow}{play_passes} lần")
                            while True:
                                common.log(f"{common.yellow}Bắt đầu chơi game")
                                start_game = self.start_game(token)
                                if start_game.status_code == 200:
                                    common.log(f"{common.green}Đang chơi game trong 30s ...")
                                    time.sleep(30)
                                    point = random.randint(500,600)
                                    claim_game = self.claim_game(token, point)
                                    if claim_game.status_code == 200:
                                        user_info = self.get_balance(token).json().get("data")
                                        balance = user_info["available_balance"]
                                        tickets_left = user_info["play_passes"]
                                        common.log(f"{common.green}Số dư hiện tại: {common.white}{balance}")
                                        common.log(f"{common.green}Vé hiện tại: {common.white}{tickets_left}")
                                        if tickets_left == 0:
                                            break
                                    else:
                                        common.log(f"{common.red}Claim point lỗi rồi")
                                else:
                                    common.log(f"{common.red}Không chơi được game")
                        else:
                            common.log(f"{common.yellow}Không đủ vé")

                    else:
                        common.log(f"{common.red}Không có token")
                except Exception as e:
                    print(f"Get auth data error!!!", e)
                print()

                if end_at_list:
                    now = datetime.now().timestamp()
                    wait_times = [end_at - now for end_at in end_at_list if end_at > now]
                    if wait_times:
                        wait_time = min(wait_times) + 30
                    else:
                        wait_time = 15 * 60
                else:
                    wait_time = 15 * 60

                wait_hours = int(wait_time // 3600)
                wait_minutes = int((wait_time % 3600) // 60)
                wait_seconds = int(wait_time % 60)

                wait_message_parts = []
                if wait_hours > 0:
                    wait_message_parts.append(f"{wait_hours} giờ")
                if wait_minutes > 0:
                    wait_message_parts.append(f"{wait_minutes} phút")
                if wait_seconds > 0:
                    wait_message_parts.append(f"{wait_seconds} giây")

                wait_message = ", ".join(wait_message_parts)
                common.log(f"{common.yellow}Hãy chờ {wait_message}!")
                countdown(int(wait_time))
                time.sleep(3)

if __name__ == "__main__":
    try:
        tomarket = Tomarket()
        tomarket.main()
    except KeyboardInterrupt:
        sys.exit()