from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from wsgisession import Session


class MongoSessionFactory(object):

    def __init__(self, database, collection='sessions', ttl=None, **kwargs):
        self.collection = MongoClient(**kwargs)[database][collection]
        self.collection.drop_indexes()
        if ttl is not None:
            self.collection.ensure_index('last_access', expireAfterSeconds=ttl)

    def load(self, id=None):
        session = Session()
        try:
            doc = self.collection.find_one({'_id': ObjectId(id)})
            if doc is not None:
                session.data = doc['data']
                session.id = id
        except:
            pass
        return session

    def save(self, session):
        doc = {
            'data': session.data,
            'last_access': datetime.utcnow(),
        }
        if session.id is not None:
            doc['_id'] = ObjectId(session.id)
        self.collection.save(doc)
        return str(doc['_id'])
