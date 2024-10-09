import json
import sys
import time
import cloudscraper
from cloudscraper import get_tokens
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
# Construct the full paths to the files
data_file = os.path.join(script_dir, "data/bits.txt")

class Bits:
    def __init__(self):
        pass
    def headers(self, token=None):
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://bits.apps-tonbox.me",
            "Pragma": "no-cache",
            "Referer": "https://bits.apps-tonbox.me/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
    def get_token(self, data):
        url = f"https://api-bits.apps-tonbox.me/api/v1/auth"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://bits.apps-tonbox.me",
            "Pragma": "no-cache",
            "Referer": "https://bits.apps-tonbox.me/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        payload = {
            "data": f"{data}"
        }
        data = json.dumps(payload)
        response = cloudscraper.create_scraper().post(url=url, data=data, headers=self.headers())
        return response

    def get_profile(self, token=None):
        url = f"https://api-bits.apps-tonbox.me/api/v1/me?access_token={token}"
        response = cloudscraper.create_scraper().get(url=url, headers=self.headers())
        return response

    def get_social_tasks(self, token=None):
        url = f"https://api-bits.apps-tonbox.me/api/v1/socialtasks?access_token={token}"
        response = cloudscraper.create_scraper().get(url=url, headers=self.headers())
        return response

    def task_start(self, token, name):
        url = f"https://api-bits.apps-tonbox.me/api/v1/socialtask/start?access_token={token}"
        payload = {
            "name": f"{name}"
        }
        data = json.dumps(payload)
        response = cloudscraper.create_scraper().post(url=url, headers=self.headers(), data=data)
        return response

    def task_claim(self, token, name):
        url = f"https://api-bits.apps-tonbox.me/api/v1/socialtask/claim?access_token={token}"
        payload = {
            "name": f"{name}"
        }
        data = json.dumps(payload)
        response = cloudscraper.create_scraper().post(url=url, headers=self.headers(), data=data)
        return response

    def main(self):
        while True:
            data = open(data_file, "r").read().splitlines()
            token = self.get_token(data=data[0]).json()
            access_token = token["token"]
            profile = self.get_profile(access_token)

            info = profile.json()
            coins = info["coins"]
            print("Coins:", coins)

            time.sleep(2)
            social_tasks = self.get_social_tasks(access_token).json()
            for social_task in social_tasks:
                if social_task["status"] == "IsDone":
                    continue
                task_name = social_task["socialTask"]["name"]
                task_start = self.task_start(access_token, task_name)
                time.sleep(1)
                task_claim = self.task_claim(access_token, task_name)
                time.sleep(1)
            print("Finish")
            wait_time = 60*60
            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        bits = Bits()
        bits.main()
    except KeyboardInterrupt:
        sys.exit()