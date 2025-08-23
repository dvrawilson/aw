import json
import os

# Define USERNAME and USERID (replace with actual values or environment variables)
# In a real scenario, these might come from environment variables or command-line args.
USERNAME = os.environ.get('USERNAME', 'example_user')
USERID = os.environ.get('USERID', '123456789')

input_file_tweets = '../data/tweets.json'
output_file_slim = '../data/slimtweets.json'
output_file_cleaned = '../data/cleanedtweets.json'

def process_tweets():
    """Reads, filters, and transforms tweet data."""
    try:
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(input_file_tweets), exist_ok=True)
        os.makedirs(os.path.dirname(output_file_slim), exist_ok=True)
        os.makedirs(os.path.dirname(output_file_cleaned), exist_ok=True)

        with open(input_file_tweets, 'r', encoding='utf-8') as f:
            tweets_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file_tweets}. Please ensure it exists.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_file_tweets}. Check file format.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    slim_tweets = []
    for item in tweets_data:
        tweet = item.get('tweet', {})

        # Filtering conditions
        in_reply_to_screen_name = tweet.get('in_reply_to_screen_name')
        in_reply_to_user_id = tweet.get('in_reply_to_user_id')
        user_mentions = tweet.get('entities', {}).get('user_mentions', [])
        retweeted_status = tweet.get('retweeted_status')
        media = tweet.get('entities', {}).get('media')
        full_text = tweet.get('full_text', '')

        # Check all conditions
        cond1 = (in_reply_to_screen_name is None or in_reply_to_screen_name == USERNAME)
        cond2 = (len(user_mentions) == 0)
        cond3 = (retweeted_status is None)
        cond4 = (in_reply_to_user_id is None or str(in_reply_to_user_id) == USERID) # Convert to string for comparison
        cond5 = (media is None)
        cond6 = (not full_text.startswith('@'))

        if cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
            # Extract and transform data
            urls_data = tweet.get('entities', {}).get('urls', [])
            formatted_urls = [
                {'url': url_item.get('url'), 'expanded': url_item.get('expanded_url')}
                for url_item in urls_data
            ]

            slim_tweets.append({
                'content': full_text,
                'timestamp': tweet.get('created_at'),
                'id': tweet.get('id'),
                'urls': formatted_urls
            })

    # Write slim_tweets to file
    try:
        with open(output_file_slim, 'w', encoding='utf-8') as f:
            json.dump(slim_tweets, f, indent=4)
        print(f"Slimmed tweets written to {output_file_slim}")
    except Exception as e:
        print(f"Error writing to {output_file_slim}: {e}")
        return

    # Second JQ step: Replace URLs in content
    cleaned_tweets = []
    for item in slim_tweets:
        content = item.get('content', '')
        urls = item.get('urls', [])

        if urls:
            for url_mapping in urls:
                original_url = url_mapping.get('url')
                expanded_url = url_mapping.get('expanded')
                if original_url and expanded_url:
                    content = content.replace(original_url, expanded_url)

        cleaned_tweets.append({
            'content': content,
            'timestamp': item.get('timestamp'),
            'id': item.get('id')
        })

    # Write cleaned_tweets to file
    try:
        with open(output_file_cleaned, 'w', encoding='utf-8') as f:
            json.dump(cleaned_tweets, f, indent=4)
        print(f"Cleaned tweets written to {output_file_cleaned}")
    except Exception as e:
        print(f"Error writing to {output_file_cleaned}: {e}")

if __name__ == "__main__":
    process_tweets()

