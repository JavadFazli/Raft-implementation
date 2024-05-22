  
import redis
import time
import json

# Connect to local Redis instance
redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
channel = 'server'

# Wait until state chnges to Candidate

# Set number_of_nodes = 3
# Answering Request vote (Accept):
message = {}
message["kind"] = "RequestVoteAnswer"
message["Answer"] = "Accept"
message["term"] = 1
message["Destination_Id"] = 0
message["id"] = 1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# Become leader :)
# Heartbeat is working :)

# Recieve message from client
message = {}
message["kind"] = "Client"
message["Entries"] = "Hi :)"
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(3)

# Recieve message from client (Again)
message = {}
message["kind"] = "Client"
message["Entries"] = "Second Hi :)"
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)

# Send Append Entries Answer (Reject)
message = {}
message["kind"] = "AppendEntriesAnswer"
message["Answer"] = "Reject"
message["term"] = 0
message["Destination_Id"] = 0
message["id"] = 1
redis_client.publish(channel, json.dumps(message, indent=4))
time.sleep(1)




