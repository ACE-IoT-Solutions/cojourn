import random
from datetime import datetime, timedelta
from typing import List
import json


def generate_sample_data(start_ts=datetime(2022, 1, 1, 0, 0), 
                         end_ts=datetime(2022, 1, 30, 0, 0),
                         sunrise_hr=6,
                         sunset_hr=18,
                         min_generation_wh=50,
                         max_generation_wh=350,
                         random_seed=10) -> List[dict]:
    random.seed(random_seed)
    data_interval_hour = 1
    start_ts = start_ts
    end_ts = end_ts
    sunrise_hr = sunrise_hr
    sunset_hr = sunset_hr
    min_generation_wh = min_generation_wh
    max_generation_wh = max_generation_wh
    samples = []
    
    current_ts = start_ts
    while current_ts < end_ts:
        generation_wh = (
        random.randint(min_generation_wh, max_generation_wh) 
        if current_ts.hour >= sunrise_hr 
        and current_ts.hour <= sunset_hr else 0
        )
        
        samples.append(
            {
               "timestamp": current_ts.isoformat(),
               "power_generated": generation_wh 
            }
        )
        current_ts += timedelta(hours=data_interval_hour)
    return samples


def write_sample_data_to_file(data: List[dict], file_name="generation_sample_data.json"):
    with open(file_name, "w") as f:
        json.dump({"generation_samples": data}, f, indent=2)


def main():
    sample_data = generate_sample_data()
    write_sample_data_to_file(sample_data)


if __name__ == "__main__":
    main()
