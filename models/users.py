import hashlib
from database import Database

class Users(object):
    def __init__(self, username):
        self.username = username

    def save_user_to_mongo(self, password_hash):
        Database.insert(collection='Users', data=self.json(password_hash))

    def json(self, password_hash):
        return {
            'username':self.username,
            'password_hash':password_hash
        }

    @staticmethod
    def check_creditentials(username, password_hash):
        return Database.find_one(collection="Users", query={'username': username,
                                                        'password_hash': str(password_hash)})

