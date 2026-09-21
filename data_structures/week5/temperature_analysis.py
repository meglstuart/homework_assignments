import json
import os
from pathlib import Path

def load_weather_data():
    with open(os.path.join(Path(__file__).parent.resolve(), 'ep_weather_data.json'), 'r') as file:
        yearly_data = json.load(file)
    return yearly_data


