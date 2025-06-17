import numpy as np
from lttb import downsample

async def downsample_logs(values: list[float | int], timestamps: list[float], target_length: int):
    # Convert values to float, handling None and invalid values
    numeric_values = []
    numeric_timestamps = []
    
    for timestamp, value in zip(timestamps, values):
        try:
            # Convert value to float, skip if conversion fails
            if value is not None:
                numeric_value = float(value)
                numeric_values.append(numeric_value)
                numeric_timestamps.append(float(timestamp))
        except (ValueError, TypeError):
            continue
    
    if not numeric_values:
        return {'timestamps_ms': [], 'values': []}
    
    data_points = np.array([(ts, val) for ts, val in zip(numeric_timestamps, numeric_values)])

    if len(data_points) <= target_length:
        return {'timestamps_ms': numeric_timestamps, 'values': numeric_values}
    
    downsampled_data = downsample(data_points, target_length)

    return {'timestamps_ms': downsampled_data[:, 0].tolist(), 'values': downsampled_data[:, 1].tolist()}