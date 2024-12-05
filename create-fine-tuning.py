import pandas as pd
import json

gt_file_path = "processed_data/train.csv"

message = [
    {
        "role": "system",
        "content": """
            You are a sentient analytical engine, 
            your goal is to analyze each tweet crawled from Twitter with the most appropriate emotion.
            The possible emotions are: anger, anticipation, disgust, fear, sadness, surprise, trust, and joy.
            There's no other emotion option, so you must choose one of these.
            The tweets contains modern slang and emojis, as well as hashtags and <LH> placeholders that you should ignore.
            You only need to output the id, and the emotion, separated by a comma and occupying a single line.
            For example, the input will be :
            tweet_id,text
            0x376b20,"People who post ""add me on #Snapchat"" must be dehydrated. Cuz man.... that's <LH>"
            0x2d5350,"@brianklaas As we see, Trump is dangerous to #freepress around the world. What a <LH> <LH> #TrumpLegacy.  #CNN"
            0x1cd5b0,Now ISSA is stalking Tasha 😂😂😂 <LH>
            0x1d755c,@RISKshow @TheKevinAllison Thx for the BEST TIME tonight. What stories! Heartbreakingly <LH> #authentic #LaughOutLoud good!!
            0x2c91a8,Still waiting on those supplies Liscus. <LH>
            ...
            
            The output should be:
            0x376b20,anticipation
            0x2d5350,sadness
            0x1cd5b0,fear
            0x1d755c,joy
            0x2c91a8,anticipation
            ...
        """
    }
]



# read gt_file_path
df = pd.read_csv(gt_file_path)
df = df.tail(1000)
df = df.drop(columns=["hashtags"])

# copy the df with the last 1000 rows, and only the tweet_id and emotion columns
respond_df = df.copy()[["tweet_id", "emotion"]]
df = df.drop(columns=["emotion"])

# create json file with messages for fine-tuning the language model
# role : user, content : 100rows from the last 1000 rows of the gt_file_path
# role : assistant, content : 100rows from the respond_df

with open("fine_tuning.json", "w") as file:
    for i in range(10):
        batch = df.iloc[i*100:(i+1)*100]
        respond_batch = respond_df.iloc[i*100:(i+1)*100]
        # convert directly to string
        user_string = batch.to_csv(index=False, sep=",")
        answer_string = respond_batch.to_csv(index=False, sep=",")
        current_message = message.copy()
        current_message.append({
            "role": "user",
            "content": user_string.strip()
        })
        current_message.append({
            "role": "assistant",
            "content": answer_string.strip()
        })
        entry = {"messages": current_message}
        file.write(json.dumps(entry) + "\n")