import time
import importlib

amizone_database = importlib.import_module('amizone-api.database')


class User:

    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.setup()

    def setup(self):
        if not amizone_database.JSONDatabase.information_exists(self.telegram_id):
            amizone_database.JSONDatabase.store_user(self.telegram_id, {'created_at': time.time()})

    def set_property(self, name, value):
        amizone_database.JSONDatabase.set(self.telegram_id, name, value)

    def get_property(self, name):
        return amizone_database.JSONDatabase.get(self.telegram_id, name)
