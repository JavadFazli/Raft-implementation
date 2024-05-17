  
import redis
import time
import json

# Connect to local Redis instance
redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
channel = 'server'

# Wait until state chnges to Candidate

# Answering Request vote (Reject):
message = {}
message["kind"] = "RequestVoteAnswer"
message["Answer"] = "Reject"
message["term"] = 1
message["Destination_Id"] = 0
message["id"] = 1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# Send Request Vote:
message = {}
message["kind"] = "RequestVote"
message["term"] = 5
message["id"]  = 5
message["Last_Log_Term"] = 5
message["Last_Log_Id"] = 5
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# Heartbeat (Must Reject)
message = {}
message["kind"] = "AppendEntries"
message["term"] = 0
message["id"]  = 1
message["Destination_Id"] = 0
message["Prev_Log_Term"] = -1
message["Prev_Log_Id"] = -1
message["Entries"] = ""
message["Leader_Commite"] = -1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# Heartbeat (Must Accept)
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

# Answering Request vote (Accept):
message = {}
message["kind"] = "RequestVoteAnswer"
message["Answer"] = "Accept"
message["term"] = 1
message["Destination_Id"] = 0
message["id"] = 1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)


