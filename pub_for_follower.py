  
import redis
import time
import json

# Connect to local Redis instance
redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
channel = 'server'

# Request vote message:
message = {}
message["kind"] = "RequestVote"
message["term"] = 1
message["id"]  = 1
message["Last_Log_Term"] = -1
message["Last_Log_Id"] = -1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# First heartbeat
message = {}
message["kind"] = "AppendEntries"
message["term"] = 2
message["id"]  = 1
message["Destination_Id"] = 0
message["Prev_Log_Term"] = -1
message["Prev_Log_Id"] = -1
message["Entries"] = ""
message["Leader_Commite"] = -1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# First Append
message = {}
message["kind"] = "AppendEntries"
message["term"] = 2
message["id"]  = 1
message["Destination_Id"] = 0
message["Prev_Log_Term"] = -1
message["Prev_Log_Id"] = -1
message["Entries"] = "First entry :)"
message["Leader_Commite"] = -1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# Second Append
message = {}
message["kind"] = "AppendEntries"
message["term"] = 2
message["id"]  = 2
message["Destination_Id"] = 0
message["Prev_Log_Term"] = 2
message["Prev_Log_Id"] = 0
message["Entries"] = "Second entry :)"
message["Leader_Commite"] = -1
redis_client.publish(channel, json.dumps(message, indent=4))

