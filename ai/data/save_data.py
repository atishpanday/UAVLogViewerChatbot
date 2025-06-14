from common.models.uavlog import UAVLog
from data.db import get_collection
from common.statistics import calculate_statistics, detect_abrupt_changes

async def save_data(uavlogs: list[UAVLog]):
    collection = get_collection()
    await collection.delete_many({})
    for log in uavlogs:
        timestamps = log.messageList.get("time_boot_ms", [])
        for metric, values in log.messageList.items():
            stats_summary = calculate_statistics(values)
            if (
                metric != "time_boot_ms" and
                isinstance(values, list)
                and len(values) == len(timestamps) and len(values) > 2
                and all(isinstance(v, (int, float)) 
                or (isinstance(v, str) and v.replace('.', '', 1).isdigit()) for v in values)
            ):
                abrupt_changes = detect_abrupt_changes(values, timestamps, 10)
                stats_summary["abrupt_changes"] = abrupt_changes
            else:
                stats_summary["abrupt_changes"] = []
            log.messageListStats[metric] = stats_summary
    uavlogs_dict = [uavlog.model_dump() for uavlog in uavlogs]
    result = await collection.insert_many(uavlogs_dict)
    return result.inserted_ids
