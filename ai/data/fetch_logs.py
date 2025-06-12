from .db import get_collection
from common.statistics import calculate_statistics, detect_abrupt_changes

async def fetch_logs(messageType: str, metrics: list[str]):
    try:
        if "time_boot_ms" not in metrics:
            metrics.append("time_boot_ms")

        projection = { "_id": 0 }
        for metric in metrics:
            projection[f"messageList.{metric}"] = 1

        collection = get_collection()
        
        result = await collection.find_one(
            {"messageType": messageType},
            projection
        )
        
        if not result:
            return []
        
        timestamps = result["messageList"]["time_boot_ms"]
            
        # Process metrics with large arrays to get statistical summaries
        for metric in metrics:
            values = result.get("messageList", {}).get(metric, [])
            if (
                isinstance(values, list)
                and len(values) == len(timestamps) and len(values) > 2
                and all(isinstance(v, (int, float)) 
                or (isinstance(v, str) and v.replace('.', '', 1).isdigit()) for v in values)
            ):
                stats_summary = calculate_statistics(values)
                abrupt_changes = detect_abrupt_changes(values, timestamps, 10)
                stats_summary["abrupt_changes"] = abrupt_changes
            else:
                stats_summary = calculate_statistics(values)
                stats_summary["abrupt_changes"] = []
            
            result["messageList"][metric] = stats_summary
        
        return result
        
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return []
    