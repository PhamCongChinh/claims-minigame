import sys, time, random, os, cloudscraper, json
from base import common, countdown

scraper = cloudscraper.create_scraper()

script_dir = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(script_dir, "data/seed.txt")
class Seed:
    def __init__(self):
        self.banner = common.create_banner(game_name="Seed")

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
        try:
            response = scraper.get(url=url, headers=self.headers(data))
            return response.json()
        except:
            return None
    def daily_login(self, data):
        url = f"https://elb.seeddao.org/api/v1/daily-login-streak"
        try:
            response = scraper.get(url=url, headers=self.headers(data))
            res = json.loads(response.text)
            return res
        except:
            return None

    def profile2(self, data):
        url = f"https://elb.seeddao.org/api/v1/profile2"
        try:
            response = scraper.get(url=url, headers=self.headers(data))
            return response.json()
        except:
            return None

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
        return response.text

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
            common.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            for no, data in enumerate(data):
                balance = self.balance(data)
                balance_data = balance["data"]
                common.log(f"{common.green}Tài sản: {common.white}{balance_data}")
                time.sleep(2)
                daily_login1 = self.profile2(data)
                print(daily_login1)


                # check_daily = self.login_bonus(data)
                # print(check_daily.json())
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

            wait_time = random.randint(30, 60)
            common.log(f"Thời gian chờ: {wait_time} giây")
            countdown(wait_time)

if __name__ == "__main__":
    try:
        seed = Seed()
        seed.main()
    except KeyboardInterrupt:
        sys.exit()