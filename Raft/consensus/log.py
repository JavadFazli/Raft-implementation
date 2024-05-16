from Raft.storage.mongo import MongoDB
class Log:
    def __init__(self):
        self.db = MongoDB()  # Initialize MongoDB connection

    def store(self, log_entry , term, index):
        """
        Store a log entry in MongoDB.

        Args:
            log_entry: Log entry to be stored.
        """
        try:
            # Check if a document with the specified term already exists
            if self.db.get_collection('log').find_one({'index': index}):
                raise ValueError("Error: A document with the specified index already exists.")
            log_document = {"log_entry": log_entry,'term': term,'index':index}  # Create a dictionary representing the log entry
            self.db.insert_one("log", log_document)
            # self.db.insert_one("log", log_entry)
            print("Log entry stored successfully.")
        except Exception as e:
            print(f"Error storing log entry: {e}")

    def load(self):
        """
        Load all log entries from MongoDB.

        Returns:
            list: List of log entries.
        """
        try:
            # log_entries = self.db.find_all("log")
            log_entries = self.db.find_all("log")  # Retrieve all log documents from the "log" collection
            # log_entries = [entry["entry"] for entry in log_entries]  # Extract the log entries from the documents
            print("Log entries loaded successfully.")
            return log_entries
        except Exception as e:
            print(f"Error loading log entries: {e}")
            return []

    def find_log_by_index(self,index):
        """
        Find a document with the  log_entry, and term.
        """
        collection=self.db.get_collection('log')
        query = {'index': index}
        result = collection.find_one(query)
        return result
    def delete_log_by_index(self, index):
        """
        Find a document with the  log_entry, and term.
        """
        collection=self.db.get_collection('log')
        query = {'index': index}
        result = collection.delete_one(query)
        return result