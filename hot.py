from claimer import Claimer

class HotClaimer(Claimer):
    def initialize_settings(self):
        super().initialize_settings()
        self.script = "games/hot.py"
        self.prefix = "HOT:"
        self.url = "https://web.telegram.org/k/#@herewalletbot"
        self.pot_full = "Filled"
        self.pot_filling = "to fill"
        self.seed_phrase = None
        self.forceLocalProxy = False
        self.forceRequestUserAgent = False
        self.step = "01"
        self.imported_seedphrase = None
        self.start_app_xpath = "//a[@href='https://t.me/herewalletbot/app'] | //div[@class='new-message-bot-commands-view'][contains(text(),'Open Wallet')]"