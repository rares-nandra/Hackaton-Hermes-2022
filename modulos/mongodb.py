import pymongo
import time

class mongodb():
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017, username="admin", password="parolacomplicata")
        self.db = self.client['SafeBreak']
        self.user = self.db.user
        self.collection = self.db.user

    def add(self, cerere):
        if not (self.collection.find_one({"user": cerere["user"]})):
            post_id = self.user.insert_one(cerere).inserted_id
            return True
        else:
            return False

    def verificareUser(self, user, parola):
        find = self.user.find_one({"user": user})
        print(find)
        if(find and find["parola"] == parola):
            return True
        else:
            return False
            
    def update(self, dict, user):
        self.user.update_one({'user': user}, {'$set' : dict})
        print(dict)

    def fileName(self, user):
        find = self.user.find_one({"user": user})
        return find['filename']

    def data(self, user):
        return self.user.find_one({"user": user})

    def favorite(self, locatie, user):
        print(locatie)
        self.user.update_one({'user': user}, {'$set' : locatie}) 


    