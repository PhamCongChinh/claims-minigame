import sys, json, time
from base import common, countdown

import cloudscraper
scraper = cloudscraper.create_scraper()

class Blum:
    def __init__(self):
        self.data_file = common.file_path(file_name="configs/blum-data.txt")
        self.line = common.create_line(length=50)
        self.banner = common.create_banner(game_name="Blum")

        self.auto_check_in = common.get_config(config_file=self.config_file, config_name="auto-check-in")

    def headers(self, token=None):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://telegram.blum.codes",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def get_token(self, data, proxies=None):
        url = f"https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
        payload = {"query": data}
        try:
            response = scraper.post(url=url,headers=self.headers(), json=payload, timeout=20)
            data = response.json()
            token = data["token"]["access"]
            return token
        except:
            return None
        
    def get_info(self, token):
        url = "https://game-domain.blum.codes/api/v1/user/balance"
        try:
            response = scraper.get(url=url,headers=self.headers(token=token))
            data = response.json()
            balance = float(data["Số dư khả dụng"])
            ticket = data["Vé chơi"]
            common.log(f"{common.green}Tài sản:  {common.white}{balance:,}")

        except:
            return None
    
    def main(self):
        while True:
            common.clear_terminal()
            print(self.banner)
            data = open(self.data_file, "r").read().splitlines()
            number_account = len(data)
            common.log(f"{common.green}Number of accounts: {common.white}{number_account}")

            for no, data in enumerate(data):
                common.log(self.line)
                common.log(f"{common.green}Account number: {common.white}{no+1}/{number_account}")

                try:
                    token = self.get_token(data=data)
                    print(token)
                except Exception as e:
                    common.log(f"{common.red}Lỗi dữ liệu: {common.white}{e}")
            
            print()
            wait_time = 60 * 60
            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        blum = Blum()
        blum.main()
    except KeyboardInterrupt:
        sys.exit()