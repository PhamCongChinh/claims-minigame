import json
import os
import sys
import time
import requests
import cloudscraper
from requests import request

scraper = cloudscraper.create_scraper()
from base import common

class MoneyDogs:
    def __init__(self):
        self.line = common.create_line(length=50)
        self.banner = common.create_banner(game_name="Money Dogs")

    def headers(self):
        return {
            "Accept-Type": "application/json",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Origin": "https://app.moneydogs-ton.com",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://app.moneydogs-ton.com/",
            "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
    def get_sessions(self):
        url = f"https://api.moneydogs-ton.com/sessions"
        payload = {
            "encodedMessage": "query_id=AAESTRtAAwAAABJNG0C8wCbH&user=%7B%22id%22%3A7517981970%2C%22first_name%22%3A%22Dao%20%F0%9F%8D%85%20%F0%9F%90%88%E2%80%8D%E2%AC%9B%20%F0%9F%8C%B1SEED%22%2C%22last_name%22%3A%22Nguyen%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1728008930&hash=0dc3a2e26ec7bca64fe45c422880f15e23bc9f105cdf874c88b12d7c1caf9769"
        }
        data = json.dumps(payload)
        response = requests.request("POST", url=url, headers=self.headers(), data=data)
        return response

    def daily_check_in(self, token):
        url = f"https://api.moneydogs-ton.com/daily-check-in"
        headers = self.headers()
        headers["X-Auth-Token"] = token
        response = scraper.get(url=url, headers=headers)
        return response

    def tasks(self, token):
        url = f"https://api.moneydogs-ton.com/tasks"
        headers = self.headers()
        headers["X-Auth-Token"] = token
        response = scraper.get(url=url, headers=headers)
        return response

    def main(self):
        while True:
            common.clear_terminal()
            print(self.line)
            print(self.banner)
            try:
                token = self.get_sessions().json()["token"]

                time.sleep(2)
                common.log("Điểm danh hằng ngày!")
                check_in = self.daily_check_in(token=token).json()
                if check_in["user"]["active"]:
                    common.log("Đã điểm danh. Đợi ngày mai nhé :))")
                else:
                    common.log("Đã điểm danh!")
            except Exception as e:
                common.log(e)
            wait_time = 60 * 60
            common.log(f"{common.yellow}Wait for {int(wait_time / 60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        moneydogs = MoneyDogs()
        moneydogs.main()
    except KeyboardInterrupt:
        sys.exit()