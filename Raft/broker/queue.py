import redis
import json


class RedisQueue:
    def __init__(self, host='localhost', port=6379, db=0):
        # Connect to the Redis server
        self.client = redis.Redis(host=host, port=port, db=db)

    def publish(self, channel, message):
        # Publish a message to a specific Redis channel
        try:
            # Convert the message to JSON if it's a dictionary or other data structure
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            self.client.publish(channel, message)
        except Exception as e:
            print(f"Error publishing to channel {channel}: {e}")
            raise e

    def subscribe(self, channel):
        # Subscribe to a specific Redis channel
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        return pubsub

    def get_message(self, pubsub, timeout=1):
        # Get the next message from the pub/sub with a timeout
        try:
            return pubsub.get_message(timeout=timeout)
        except Exception as e:
            print(f"Error getting message from pub/sub: {e}")
            raise e

    def close(self):
        # Close the Redis connection
        self.client.close()
