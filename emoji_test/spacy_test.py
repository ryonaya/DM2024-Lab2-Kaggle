import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("emoji", first=True)

# # read text file
# with open("unique_emojis_train.txt", "r", encoding="utf-8") as file:
#     text = file.read()
    
# # process text
# doc = nlp(text)

# # save emojis and their descriptions to a csv file
# with open("emojis_descriptions_train.csv", "w", encoding="utf-8") as file:
#     file.write("Emoji,Description\n")
#     for emoji in doc._.emoji:
#         symbol, index, description = emoji
#         file.write(f"{symbol},{description}\n")
    
# read processed_data/train.csv 
# convert emojis to their descriptions and quote them inside brackets
import pandas as pd
import re

df = pd.read_csv("processed_data/train.csv")
# tweet_id, text, hashtags, emotion