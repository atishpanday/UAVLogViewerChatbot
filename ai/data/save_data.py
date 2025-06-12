from common.models.uavlog import UAVLog
from data.db import get_collection

async def save_data(uavlogs: list[UAVLog]):
    collection = get_collection()
    await collection.delete_many({})
    uavlogs_dict = [uavlog.model_dump() for uavlog in uavlogs]
    result = await collection.insert_many(uavlogs_dict)
    return result.inserted_ids
