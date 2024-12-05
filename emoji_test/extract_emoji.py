import csv
import re

def extract_unicode_emojis_from_csv(input_csv, output_txt):
    # Define a regular expression to match Unicode surrogate pairs and standard emojis
    unique_emojis = set()

    # Read the CSV file
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for cell in row:
                # Find all matches of emojis in the cell
                emojis = extract_emojis(cell)
                unique_emojis.update(emojis)

    # Write the unique emojis to a text file
    with open(output_txt, 'w', encoding='utf-8') as txtfile:
        for emoji in sorted(unique_emojis):  # Sort results for readability
            txtfile.write(emoji + '\n')

    print(f"Extracted {len(unique_emojis)} unique emojis to {output_txt}")

def extract_emojis(text):
    """
    Extract unique emojis from text, properly handling compound emojis, modifiers,
    and sequential emoji combinations.
    
    Args:
        text (str): Input text containing emojis
        
    Returns:
        list: List of unique emojis found in the text
    """
    # Emoji modifier ranges
    EMOJI_MODIFIERS = re.compile(r'[\U0001F3FB-\U0001F3FF]')
    
    def is_emoji_modifier(char):
        """Check if the character is an emoji modifier (like skin tone)."""
        return '\U0001F3FB' <= char <= '\U0001F3FF'
    
    def get_emoji_and_modifier(text, start):
        """Extract a single emoji with its modifier if present."""
        char = text[start]
        next_char = text[start + 1] if start + 1 < len(text) else None
        
        # If next character is a modifier, include it
        if next_char and is_emoji_modifier(next_char):
            return char + next_char, start + 2
        return char, start + 1
    
    def split_into_emojis(text):
        """Split text into individual emojis, properly handling modifiers."""
        emojis = []
        i = 0
        
        while i < len(text):
            emoji, next_pos = get_emoji_and_modifier(text, i)
            emojis.append(emoji)
            i = next_pos
            
        return emojis
    
    # First, find emoji sequences using a comprehensive pattern
    emoji_pattern = re.compile(
        r'['
        r'\U0001F1E0-\U0001F1FF'  # flags (regional indicators)
        r'\U0001F300-\U0001F5FF'  # symbols & pictographs
        r'\U0001F600-\U0001F64F'  # emoticons
        r'\U0001F680-\U0001F6FF'  # transport & map symbols
        r'\U0001F700-\U0001F77F'  # alchemical symbols
        r'\U0001F780-\U0001F7FF'  # geometric shapes
        r'\U0001F800-\U0001F8FF'  # supplemental arrows
        r'\U0001F900-\U0001F9FF'  # supplemental symbols & pictographs
        r'\U0001FA00-\U0001FA6F'  # chess symbols
        r'\U0001FA70-\U0001FAFF'  # symbols & pictographs extended-A
        r'\U00002702-\U000027B0'  # dingbats
        r'\U000024C2-\U0001F251'
        r'\u2600-\u26FF'          # misc symbols including ☝
        r'\u2700-\u27BF'          # dingbats
        r'\u2B50\u2B55'           # additional symbols
        ']+',
        flags=re.UNICODE
    )

    # Find all emoji sequences and process them
    unique_emojis = set()
    for match in emoji_pattern.finditer(text):
        sequence = match.group()
        emojis = split_into_emojis(sequence)
        unique_emojis.update(emojis)
    
    return sorted(list(unique_emojis))

input_csv = 'processed_data/test.csv'
output_txt = 'unique_emojis_test.txt'  # Output file for the extracted emojis
extract_unicode_emojis_from_csv(input_csv, output_txt)

input_csv = 'processed_data/train.csv'
output_txt = 'unique_emojis_train.txt'  # Output file for the extracted emojis
extract_unicode_emojis_from_csv(input_csv, output_txt)