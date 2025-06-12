from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv(".env")

def get_collection():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client["uavlogs"]
    collection = db["telemetry"]
    return collection