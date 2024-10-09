import json
import sys
import time
import random

import cloudscraper
scraper = cloudscraper.create_scraper()
from base import common


code = "user={\"id\":7517981970,\"first_name\":\"Dao 🍅 🐈‍⬛ 🌱SEED\",\"last_name\":\"Nguyen\",\"language_code\":\"en\",\"allows_write_to_pm\":true}&chat_instance=8408761834560869409&chat_type=sender&auth_date=1728051857&hash=a006281bb47e1cd2aea60161229562c97dfee6a939824173e9b8e3d98a2d1bb3"
url_login = f"https://api-backend.yescoin.gold/user/login"
url_get_account_info = f"https://api-backend.yescoin.gold/account/getAccountInfo"
url_collect_coin = f"https://api-backend.yescoin.gold/game/collectCoin"

class YesCoin:
    def __init__(self):
        self.banner = common.create_banner(game_name="Yes Coin")

    def headers(self, token=None):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "Origin": "https://www.yescoin.gold",
            "Referer": "https://www.yescoin.gold/",
            "Token": f"{token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }

    def login(self):
        data = json.dumps({
            "code": code
        })
        return scraper.post(url=url_login, headers=self.headers(), data=data)

    def get_account_info(self, token=None):
        response = scraper.get(url=url_get_account_info, headers=self.headers(token))
        return response.json()

    def collect_coin(self, point, token=None):
        response = scraper.post(url=url_collect_coin, headers=self.headers(token), data=f"{point}")
        return response.json()

    def daily_checkin(self, token=None):
        url = f"https://api-backend.yescoin.gold/signIn/claim"
        data = json.dumps({
            "createAt": time.time(),
            "destination": "",
            "id": "1842223123498979328",
            "signInType": 1
        })
        response = scraper.post(url=url, headers=self.headers(token=token), data=data)
        return response.json()

    def full_recovery(self, token):
        url = f"https://api-backend.yescoin.gold/game/recoverCoinPool"
        response = scraper.post(url=url, headers=self.headers(token=token))
        return response.json()

    def recover_special_box(self, token):
        url = f"https://api-backend.yescoin.gold/game/recoverSpecialBox"
        response = scraper.post(url=url, headers=self.headers(token))
        return response.json()

    def get_special_box_info(self, token):
        url = f"https://api-backend.yescoin.gold/game/getSpecialBoxInfo"
        response = scraper.get(url=url, headers=self.headers(token))
        return response.json()

    def get_task_list(self, token):
        url = f"https://api-backend.yescoin.gold/task/getTaskList"
        response = scraper.get(url=url, headers=self.headers(token))
        return response.json()
    def click_task(self, token, data):
        url = f"https://api-backend.yescoin.gold/task/clickTask"
        response = scraper.post(url=url, headers=self.headers(token), data=data)
        return response.json()
    def check_task(self, token, data):
        url = f"https://api-backend.yescoin.gold/task/checkTask"
        response = scraper.post(url=url, headers=self.headers(token), data=data)
        return response.json()
    def claim_task(self, token, data):
        url = f"https://api-backend.yescoin.gold/task/claimTaskReward"
        response = scraper.post(url=url, headers=self.headers(token), data=data)
        return response.json()

    def main(self):
        while True:
            print(self.banner)
            login = self.login().json()
            token = login["data"]["token"]
            if token:
                info = self.get_account_info(token)
                # Get Account Info
                common.log(f'Total Amount: {common.blue}{info["data"]["totalAmount"]}')
                common.log(f'Current Amount: {common.blue}{info["data"]["currentAmount"]}')

                # Check in
                check_in = self.daily_checkin(token)
                if check_in["code"] == 200:
                    common.log(f'Reward: {check_in["data"]["reward"]}')
                else:
                    common.log(f"Rewarded!")

                time.sleep(1)
                recover_special_box = self.recover_special_box(token)
                special_box = self.get_special_box_info(token)
                full_recovery = self.full_recovery(token=token)

                time.sleep(1)
                task_list = self.get_task_list(token)
                if task_list["code"] == 0:
                    task_array = task_list["data"]["taskList"]
                    for task in task_array:
                        self.click_task(token, task["taskId"])
                        time.sleep(2)
                        self.click_task(token, task["taskId"])
                        time.sleep(2)
                        self.claim_task(token, task["taskId"])



                # Collect Coin
                time.sleep(1)
                while True:
                    point = random.randint(10,200)
                    collect_coin = self.collect_coin(point, token)
                    common.log(collect_coin["data"]["currentAmount"])
                    time.sleep(random.randint(10,30))


            wait_time = 60 * 60
            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        yescoin = YesCoin()
        yescoin.main()
    except KeyboardInterrupt:
        sys.exit()