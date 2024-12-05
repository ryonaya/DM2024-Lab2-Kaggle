import json
import csv
from typing import Dict, List, Set
import logging
from pathlib import Path

def setup_logging():
    """Configure logging for the data processing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_emotion_mapping(emotion_file: str) -> Dict[str, str]:
    """
    Load emotion labels from CSV file
    Returns: Dict[tweet_id, emotion]
    """
    emotion_map = {}
    logging.info(f"Loading emotion mappings from {emotion_file}")
    
    with open(emotion_file, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            tweet_id = row[0]
            emotion = row[1]
            emotion_map[tweet_id] = emotion
    
    logging.info(f"Loaded {len(emotion_map)} emotion mappings")
    return emotion_map

def load_identification_mapping(identification_file: str) -> Set[str]:
    """
    Load test set identification from CSV file
    Returns: Set of test tweet IDs
    """
    test_ids = set()
    logging.info(f"Loading identification mappings from {identification_file}")
    
    with open(identification_file, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            tweet_id = row[0]
            id_type = row[1]
            if id_type.lower() == 'test':
                test_ids.add(tweet_id)
    
    logging.info(f"Loaded {len(test_ids)} test IDs")
    return test_ids

def process_tweets(
    input_file: str,
    emotion_map: Dict[str, str],
    test_ids: Set[str],
    train_output: str,
    test_output: str
):
    """
    Process tweets and split into train/test files
    """
    train_count = 0
    test_count = 0
    skipped_count = 0
    
    # Create output directories if they don't exist
    Path(train_output).parent.mkdir(parents=True, exist_ok=True)
    Path(test_output).parent.mkdir(parents=True, exist_ok=True)
    
    with open(train_output, 'w') as train_file, \
         open(test_output, 'w') as test_file:
        
        logging.info(f"Processing tweets from {input_file}")
        
        with open(input_file, 'r') as f:
            for line in f:
                try:
                    tweet_data = json.loads(line.strip())
                    tweet_id = tweet_data['_source']['tweet']['tweet_id']
                    
                    # Write to appropriate file
                    if tweet_id in test_ids:
                        # For test set, we don't include emotion
                        json.dump(tweet_data, test_file)
                        test_file.write('\n')
                        test_count += 1
                    elif tweet_id in emotion_map:
                        # For training set, include emotion if we have it
                        tweet_data['emotion'] = emotion_map[tweet_id]
                        json.dump(tweet_data, train_file)
                        train_file.write('\n')
                        train_count += 1
                    else:
                        skipped_count += 1
                        
                except json.JSONDecodeError:
                    logging.error(f"Failed to parse JSON: {line[:100]}...")
                    continue
                except KeyError as e:
                    logging.error(f"Missing key {e} in tweet: {line[:100]}...")
                    continue
    
    logging.info(f"Processed tweets: {train_count + test_count + skipped_count}")
    logging.info(f"Training set: {train_count} tweets")
    logging.info(f"Test set: {test_count} tweets")
    logging.info(f"Skipped: {skipped_count} tweets")

def main():
    # Configuration
    INPUT_FILE = "tweets_DM.json"
    EMOTION_FILE = "emotion.csv"
    IDENTIFICATION_FILE = "data_identification.csv"
    TRAIN_OUTPUT = "processed_data/train.json"
    TEST_OUTPUT = "processed_data/test.json"
    
    setup_logging()
    
    # Load mappings
    emotion_map = load_emotion_mapping(EMOTION_FILE)
    test_ids = load_identification_mapping(IDENTIFICATION_FILE)
    
    # Process tweets
    process_tweets(
        INPUT_FILE,
        emotion_map,
        test_ids,
        TRAIN_OUTPUT,
        TEST_OUTPUT
    )

if __name__ == "__main__":
    main()