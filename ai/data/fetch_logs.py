from .db import get_collection
from common.downsample_logs import downsample_logs

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
        
        timestamps = result["messageList"].get("time_boot_ms", [])

        if not timestamps:
            return []

        final_data = {}

        for metric in metrics:
            if metric == "time_boot_ms":
                continue
            
            values = result["messageList"][metric]
            
            downsampled_data = await downsample_logs(values, timestamps, 100)

            final_data[metric] = downsampled_data
        
        return final_data
        
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return []
    