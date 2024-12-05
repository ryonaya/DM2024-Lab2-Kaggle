from openai import OpenAI
import tiktoken
import pandas as pd

file_path = "gpt_example_50.csv"
gt_file_path = "processed_data/train.csv"
# model_name = "gpt-4o-mini"
model_name = "ft:gpt-4o-mini-2024-07-18:daidai-s:10x100:AaR6aFxc:ckpt-step-10"
client = OpenAI(api_key=None)

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

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def append_message_patch(content: str) -> None:
    """Appends a message patch to the message list."""
    message_patch = {
        "role": "user",
        "content": content
    }
    message.append(message_patch)

def num_tokens_from_file(file_path: str) -> int:
    """Returns the number of tokens in a text file."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    append_message_patch(text)
    total_tokens = 0
    for m in message:
        total_tokens += num_tokens_from_string(m["content"])
    return total_tokens


# print(num_tokens_from_file(file_path))

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()
append_message_patch(text)

completion = client.chat.completions.create(
    model=model_name,
    messages=message
)

print(completion.choices[0].message.content)
result_string = completion.choices[0].message.content

# save the result to a file
header = "id,emotion\n"
with open("result.csv", "w", encoding="utf-8") as file:
    file.write(header)
    file.write(result_string)

# check the accuracy of the model
df = pd.read_csv("result.csv")
# remove first row if the first row looks like "tweet_id,text_id"
if df.iloc[0, 0] == "tweet_id":
    df = df.drop(0)
gt_df = pd.read_csv(gt_file_path)

correct = 0
for i, row in df.iterrows():
    tweet_id = row["id"]
    emotion = row["emotion"].strip()
    gt_emotion = gt_df[gt_df["tweet_id"] == tweet_id]["emotion"].values[0]
    if emotion == gt_emotion:
        correct += 1

accuracy = correct / len(df)
print(f"Accuracy: {accuracy}")

