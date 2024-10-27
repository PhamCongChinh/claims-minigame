class Claimer:
    def __init__(self):
        self.initialize_settings()

    def initialize_settings(self):
        self.settings_file = "variables.txt"
        self.status_file_path = "status.txt"
        self.start_app_xpath = None
        self.settings = {}
        self.driver = None
        self.target_element = None
        self.random_offset = 0
        self.seed_phrase = None
        self.wallet_id = ""
        self.script = "default_script.py"
        self.prefix = "Default:"
        self.allow_early_claim = True
        self.default_platform = "web"