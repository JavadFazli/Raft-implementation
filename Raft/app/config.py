import os
from dotenv import load_dotenv
import json


# Load environment variables from .env file
load_dotenv()

# Configuration class for the project

class Config:
    GRPC_PORT = int(os.getenv("GRPC_PORT"))  # Ensure it's converted to an integer
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    RAFT_NODE_PORT=int(os.getenv("RAFT_NODE_PORT"))
    RAFT_NODE_HOST=os.getenv("RAFT_NODE_HOST")
    NODE_PORTS = json.loads(os.getenv("NODE_PORTS"))
    NODE_PORTS = {int(key): int(value) for key, value in NODE_PORTS.items()}
    REDIS_URI=os.getenv("REDIS_URI")
    NODE_HOSTS= json.loads(os.getenv("NODE_HOSTS"))
    NODE_HOSTS = {int(key): value for key, value in NODE_HOSTS.items()}

    # Additional configuration