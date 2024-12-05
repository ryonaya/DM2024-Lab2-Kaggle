import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict

data_path = "fine_tuning.json"

# Load the dataset
dataset = []
with open(data_path, "r") as file:
    for line in file:
        dataset.append(json.loads(line))

# Initial dataset stats
print("Num examples:", len(dataset))
print("First example:")
for message in dataset[0]["messages"]:
    print(message)