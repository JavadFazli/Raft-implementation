import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration class for the project

class Config:
    GRPC_PORT = int(os.getenv("GRPC_PORT"))  # Ensure it's converted to an integer
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    # Additional configuration