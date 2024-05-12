from storage.mongo import MongoDB
class Log:
    def __init__(self):
        self.db = MongoDB()  # Initialize MongoDB connection

    def store(self, log_entry):
        """
        Store a log entry in MongoDB.

        Args:
            log_entry (dict): Log entry to be stored.
        """
        try:
            log_document = {"entry": log_entry}  # Create a dictionary representing the log entry
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
            log_entries = [entry["entry"] for entry in log_entries]  # Extract the log entries from the documents
            print("Log entries loaded successfully.")
            return log_entries
        except Exception as e:
            print(f"Error loading log entries: {e}")
            return []
