import numpy as np

def calculate_statistics(values: list[int | float]):
    numeric_values = []
    for v in values:
        try:
            numeric_values.append(float(v))
        except (ValueError, TypeError):
            continue

    if not numeric_values:
        return {
            "min": None,
            "max": None,
            "mean": None,
            "median": None,
            "std": None,
            "variance": None,
            "percentile_25": None,
            "percentile_75": None
        }

    values_array = np.array(numeric_values)
    stats_summary = {
        "min": float(np.min(values_array)),
        "max": float(np.max(values_array)), 
        "mean": float(np.mean(values_array)),
        "median": float(np.median(values_array)),
        "std": float(np.std(values_array)),
        "variance": float(np.var(values_array)),
        "percentile_25": float(np.percentile(values_array, 25)),
        "percentile_75": float(np.percentile(values_array, 75))
    }
    return stats_summary

def detect_abrupt_changes(values: list[float], timestamps: list[float], threshold_factor: int = 10):
    if len(values) < 2:
        return []
        
    values_array = np.array(values)
    changes = []
    
    window = max(10, len(values) // 10)
    rolling_std = np.std(values_array[:window])  # Initial std dev
    
    for i in range(1, len(values)):
        value_change = abs(values[i] - values[i-1])
        
        # Update rolling std dev
        if i >= window:
            rolling_std = np.std(values_array[i-window:i])
            
        # Check if change is greater than threshold_factor times rolling std dev
        if rolling_std > 0 and value_change > (threshold_factor * rolling_std):
            changes.append({
                "index": i,
                "timestamp_ms": timestamps[i],
                "initial_value": values[i-1],
                "final_value": values[i],
                "change_magnitude": value_change
            })
            
    return changes
