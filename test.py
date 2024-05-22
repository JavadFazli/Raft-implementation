from Raft.storage.mongo import MongoDB
from Raft.rpc.client import RaftClient
from Raft.consensus.log import Log

# data_base = MongoDB()
# print(data_base.get_collection("hi"))

# client = RaftClient()
log = Log()

# message = {}
# message["kind"] = "AppendEntries"
# message["term"] = 2
# message["id"]  = 1
# message["Destination_Id"] = 0
# message["Prev_Log_Term"] = -1
# message["Prev_Log_Id"] = -1
# message["Entries"] = "First entry :)"
# message["Leader_Commite"] = -1
# message["index"] = 0

# log.store(message)

message = log.find_log_by_index(0)
print(message)