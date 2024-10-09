import sys
import time
import random

import cloudscraper
scraper = cloudscraper.create_scraper()
from base import common

class Seed:
    def __init__(self):
        pass

    def headers(self, query_id):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "Origin": "https://cats-frontend.tgapps.store",
            "Referer": "https://cats-frontend.tgapps.store/",
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
            query_id = f"query_id=AAESTRtAAwAAABJNG0D0mg26&user=%7B%22id%22%3A7517981970%2C%22first_name%22%3A%22Dao%20%F0%9F%8D%85%20%F0%9F%90%88%E2%80%8D%E2%AC%9B%20%F0%9F%8C%B1SEED%22%2C%22last_name%22%3A%22Nguyen%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1728462449&hash=1c2ea74848e7957f58e56562f3e35e6eb2cd36bdfa3e3f5f28487af0330b1fab"
            balance = self.balance(query_id).json()
            common.log(f"{common.blue}Balance: {balance['data']}")

            time.sleep(1)
            # Get worms
            worms = self.get_worms(query_id).json()
            next_worm = worms["data"]["next_worm"]
            common.log(f"Next worm: {next_worm}")

            time.sleep(1)
            claim = self.claim(query_id).json()
            if claim["code"] == "invalid-request":
                common.log("Claim too early!")
            else:
                amount = claim["data"]["amount"]
                common.log(f"Amount claim: {amount}")

            # check daily
            time.sleep(1)
            check_daily = self.login_bonus(query_id).json()
            day = check_daily["data"][0]["no"]
            common.log(f"Kiem tra ngay thu: {day}")

            time.sleep(1)
            tasks = self.get_tasks(query_id).json()
            task_list = tasks["data"]

            for task in task_list:
                time.sleep(random.randint(5,20))
                claim_task = self.get_task(query_id, task["id"])
                task_name = task["name"]
                common.log(f"{task_name} is completed!")

            wait_time = random.randint(3600, 7200)
            common.log(f"Wait time: {wait_time} minutes")
            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        seed = Seed()
        seed.main()
    except KeyboardInterrupt:
        sys.exit()