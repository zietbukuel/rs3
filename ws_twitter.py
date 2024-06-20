import pandas as pd
from ntscraper import Nitter
import time

# List of Nitter instances to try
nitter_instances = [
    "https://nitter.net",
    "https://nitter.privacydev.net",
    "https://nitter.42l.fr",
    "https://nitter.snopyta.org",
    "https://nitter.moomoo.me"
]

# Function to fetch tweets based on query, mode, and number of tweets
def get_tweets(scraper, query, modes, no):
    tweets = scraper.get_tweets(query, mode=modes, number=no)
    final_tweets = []
    for x in tweets['tweets']:
        data = [x['link'], x['text'], x['date'], x['stats']['likes'], x['stats']['comments']]
        final_tweets.append(data)
    dat = pd.DataFrame(final_tweets, columns=['twitter_link', 'text', 'date', 'likes', 'comments'])
    return dat

# List of queries related to security topics in Peru
queries = ["robbery", "crime", "assault", "insecurity","Peru"]

# Collect tweets for each query and combine into a single DataFrame
all_tweets = pd.DataFrame()

for instance in nitter_instances:
    try:
        # Initialize the scraper
        scraper = Nitter(0)
        scraper.instance = instance  # Set the instance manually
        print(f"Trying instance: {instance}")
        for query in queries:
            tweets = get_tweets(scraper, query, 'hashtag', 100)
            if not tweets.empty:
                all_tweets = pd.concat([all_tweets, tweets], ignore_index=True)
        if not all_tweets.empty:
            break
    except Exception as e:
        print(f"Error with instance {instance}: {e}")
        time.sleep(5)  # Wait for 5 seconds before trying the next instance

# Save the combined DataFrame to a CSV file
if not all_tweets.empty:
    all_tweets.to_csv('security_tweets_peru.csv', index=False)
    print("Saved tweets to security_tweets_peru.csv")
else:
    print("No tweets fetched. Please try again later.")

# Display the DataFrame
print(all_tweets.head())
