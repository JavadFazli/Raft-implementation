from pymongo import MongoClient
from pymongo.errors import PyMongoError
from app.config import Config

class MongoDB:
    def __init__(self):
        # Establish a connection to MongoDB
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.MONGO_DB_NAME]
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e

    def get_collection(self, collection_name):
        # Get a specific collection from MongoDB
        return self.db[collection_name]

    def insert_one(self, collection_name, document):
        # Insert a single document into a collection
        collection = self.get_collection(collection_name)
        try:
            collection.insert_one(document)
        except PyMongoError as e:
            print(f"Error inserting document into {collection_name}: {e}")
            raise e

    def find_one(self, collection_name, query):
        # Find a single document based on a query
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def find_all(self, collection_name, query={}):
        # Find all documents that match the query
        collection = self.get_collection(collection_name)
        return list(collection.find(query))

    def update_one(self, collection_name, query, update):
        # Update a single document based on a query
        collection = self.get_collection(collection_name)
        try:
            collection.update_one(query, update)
        except PyMongoError as e:
            print(f"Error updating document in {collection_name}: {e}")
            raise e

    def delete_one(self, collection_name, query):
        # Delete a single document based on a query
        collection = self.get_collection(collection_name)
        try:
            collection.delete_one(query)
        except PyMongoError as e:
            print(f"Error deleting document from {collection_name}: {e}")
            raise e
