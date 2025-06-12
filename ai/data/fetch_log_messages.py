from data.db import get_collection

async def fetch_log_messages():
    collection = get_collection()

    results = collection.find({}, {"messageType": 1, "messageList": 1, "_id": 0})

    log_messages = []
    async for result in results:
        log_messages.append({
            "message_type": result["messageType"],
            "metrics": list(result["messageList"].keys())
        })

    return log_messages