import pandas as pd
import json

with open(r'runs\detect\val35\predictions.json') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        df.to_csv("validation_results.csv")