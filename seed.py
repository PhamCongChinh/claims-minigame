import sys
import time
import random
import os
import cloudscraper
import json
scraper = cloudscraper.create_scraper()
from base import common, countdown

script_dir = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(script_dir, "data/seed.txt")
class Seed:
    def __init__(self):
        pass

    def headers(self, query_id):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://cf.seeddao.org",
            "Referer": "https://cf.seeddao.org/",
            "Telegram-Data": f"{query_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }

    def balance(self, data):
        url = f"https://elb.seeddao.org/api/v1/profile/balance"
        response = scraper.get(url=url, headers=self.headers(data))
        return response

    def get_worms(self, data):
        url = f"https://elb.seeddao.org/api/v1/worms"
        response = scraper.get(url=url, headers=self.headers(data))
        return response

    def claim(self, data):
        url = f"https://elb.seeddao.org/api/v1/seed/claim"
        response = scraper.post(url=url, headers=self.headers(data))
        return response

    def login_bonus(self, data):
        url = f"https://elb.seeddao.org/api/v1/login-bonuses"
        response = scraper.get(url=url, headers=self.headers(data))
        print(response)
        return response

    def get_tasks(self, data):
        url = f"https://elb.seeddao.org/api/v1/tasks/progresses"
        response = scraper.get(url=url, headers=self.headers(data))
        return response
    def get_task(self, query_id, data):
        url = f"https://elb.seeddao.org/api/v1/tasks/{data}"
        response = scraper.post(url=url, headers=self.headers(query_id))
        return response
    def main(self):
        while True:
            data = open(data_file, "r").read().splitlines()
            for no, data in enumerate(data):
                try:
                    balance = self.balance(data).json()
                    balance_data = balance["data"]
                    common.log(f"{common.blue}Tài sản: {balance_data}")
                except Exception as e:
                    common.log(e)

                check_daily = self.login_bonus(data)
                print(check_daily.json())
                # try:
                #     time.sleep(1)
                #
                #     print(check_daily)
                #     # day = check_daily["data"][0]["no"]
                #     # common.log(f"Kiem tra ngay thu: {day}")
                # except Exception as e:
                #     common.log("alla")


            time.sleep(1)
            # # Get worms
            # try:
            #     worms = self.get_worms(query_id).json()
            #     next_worm = worms["data"]["next_worm"]
            #     common.log(f"Next worm: {next_worm}")
            # except Exception as e:
            #     common.log(e)
            #
            # time.sleep(1)
            # try:
            #     claim = self.claim(query_id).json()
            #     if claim["code"] == "invalid-request":
            #         common.log("Claim too early!")
            #     else:
            #         amount = claim["data"]["amount"]
            #         common.log(f"Amount claim: {amount}")
            # except Exception as e:
            #     common.log(e)
            #
            # # check daily

            #
            # try:
            #     time.sleep(1)
            #     tasks = self.get_tasks(query_id).json()
            #     task_list = tasks["data"]
            #
            #     for task in task_list:
            #         time.sleep(random.randint(5,20))
            #         claim_task = self.get_task(query_id, task["id"])
            #         task_name = task["name"]
            #         common.log(f"{task_name} is completed!")
            # except Exception as e:
            #     common.log(e)

            wait_time = random.randint(10, 20)
            common.log(f"Thời gian chờ: {wait_time} giây")
            countdown(wait_time)

if __name__ == "__main__":
    try:
        seed = Seed()
        seed.main()
    except KeyboardInterrupt:
        sys.exit()