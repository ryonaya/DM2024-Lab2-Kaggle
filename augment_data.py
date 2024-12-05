# read gpt_example.csv
# remove hashtags column
# save to gpt_example_no_hashtags.csv

import pandas as pd

file_path = "gpt_example.csv"
output_file_path = "gpt_example_no_hashtags.csv"

df = pd.read_csv(file_path)
df = df.drop(columns=["hashtags"])
df.to_csv(output_file_path, index=False)
print("File saved to", output_file_path)
