import sys
import time

import cloudscraper
scraper = cloudscraper.create_scraper()
from base import common

class Cats:
    def __init__(self):
        pass

    def headers(self):
        query_id = f"tma query_id=AAESTRtAAwAAABJNG0DCqyyt&user=%7B%22id%22%3A7517981970%2C%22first_name%22%3A%22Dao%20%F0%9F%8D%85%20%F0%9F%90%88%E2%80%8D%E2%AC%9B%20%F0%9F%8C%B1SEED%22%2C%22last_name%22%3A%22Nguyen%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1728226677&hash=26520c949f88e2010deff1709ada7ab0913168440ba8ac0bb1feaf009536f7c2"
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "Origin": "https://cats-frontend.tgapps.store",
            "Referer": "https://cats-frontend.tgapps.store/",
            "Authorization": f"{query_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }

    def get_user(self):
        url = f"https://api.catshouse.club/user"
        response = scraper.get(url=url, headers=self.headers())
        return response

    def get_tasks(self):
        url = f"https://api.catshouse.club/tasks/user?group=cats"
        response = scraper.get(url=url, headers=self.headers())
        return response

    def complete_task(self, task_id):
        url = f"https://api.catshouse.club/tasks/{task_id}/complete"
        response = scraper.post(url=url, headers=self.headers())
        return response

    def main(self):
        user = self.get_user().json()
        total_rewards = user["totalRewards"]
        current_rewards = user["currentRewards"]
        print(total_rewards)
        print(current_rewards)

        tasks = self.get_tasks().json()
        for task in tasks["tasks"]:
            time.sleep(0.5)
            task_id = task["id"]
            print(task_id)
            if not task["completed"]:
                continue
            else:
                complete = self.complete_task(task_id).json()
                time.sleep(3)
                print(complete)
                # time.sleep(0.5)
                # if complete["success"]:
                #     common.log(f'{complete["title"]} completed!')



if __name__ == "__main__":
    try:
        cats = Cats()
        cats.main()
    except KeyboardInterrupt:
        sys.exit()