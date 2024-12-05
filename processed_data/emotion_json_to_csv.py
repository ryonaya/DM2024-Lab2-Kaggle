import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

def setup_logging():
    """Configure logging for the conversion process"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def json_to_csv(input_file: str, output_file: str, is_train: bool = True):
    """
    Convert JSON file to CSV format
    Args:
        input_file: Path to input JSON file
        output_file: Path to output CSV file
        is_train: Boolean indicating if this is training data (includes emotion)
    """
    # Create output directory if it doesn't exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    processed = 0
    logging.info(f"Converting {input_file} to CSV format")
    
    # Define headers based on whether it's training or test data
    headers = ['tweet_id', 'text', 'hashtags']
    if is_train:
        headers.append('emotion')
    
    with open(input_file, 'r', encoding='utf-8') as json_file, \
         open(output_file, 'w', encoding='utf-8', newline='') as csv_file:
        
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        
        for line in json_file:
            try:
                tweet_data = json.loads(line.strip())
                
                # Clean and normalize the text
                text = tweet_data['_source']['tweet']['text']
                # Replace newlines and carriage returns with space
                text = text.replace('\n', ' ').replace('\r', ' ')
                # Remove extra whitespace
                text = ' '.join(text.split())
                
                # Extract the required fields
                row = {
                    'tweet_id': tweet_data['_source']['tweet']['tweet_id'],
                    'text': text,
                    'hashtags': '|'.join(tweet_data['_source']['tweet']['hashtags']) if tweet_data['_source']['tweet']['hashtags'] else ''
                }
                
                # Add emotion for training data
                if is_train:
                    row['emotion'] = tweet_data['emotion']
                
                writer.writerow(row)
                processed += 1
                
                if processed % 100000 == 0:
                    logging.info(f"Processed {processed} tweets")
                    
            except json.JSONDecodeError:
                logging.error(f"Failed to parse JSON: {line[:100]}...")
                continue
            except KeyError as e:
                logging.error(f"Missing key {e} in tweet: {line[:100]}...")
                continue
            
    logging.info(f"Finished processing {processed} tweets")
    logging.info(f"Output saved to {output_file}")

def main():
    # Configuration
    TRAIN_JSON = "processed_data/train.json"
    TEST_JSON = "processed_data/test.json"
    TRAIN_CSV = "processed_data/train.csv"
    TEST_CSV = "processed_data/test.csv"
    
    setup_logging()
    
    # Convert training data
    json_to_csv(TRAIN_JSON, TRAIN_CSV, is_train=True)
    
    # Convert test data
    json_to_csv(TEST_JSON, TEST_CSV, is_train=False)

if __name__ == "__main__":
    main()