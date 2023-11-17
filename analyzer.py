
from Tweet_Scrapper import get_tweets
from sanly import sentiment_analysis
from youtube_stats import yt_stats
import pandas as pd
import numpy as np
import json

def tweet_analysis(tweet_key):
    tweet_output = get_tweets(tweet_key)
    # print(tweet_output)
    if tweet_output not in ['error', 'no_tweet']:
        tweet_csv = pd.read_csv(tweet_output)
        snippets = tweet_csv['snippet'].tolist()
        sanly_score = sentiment_analysis(snippets)

        # Add label and score columns to the DataFrame
        tweet_csv['label'] = [item['label'] for item in sanly_score]
        tweet_csv['score'] = [item['score'] for item in sanly_score]

        # Save the DataFrame to the CSV file
        tweet_csv.to_csv(tweet_output, index=False)
        
        # Calculate the average positive score from csv]
        tweet_pos_score = tweet_csv[tweet_csv['label'] == 'positive']['score'].mean()
        tweet_neg_score = tweet_csv[tweet_csv['label'] == 'negative']['score'].mean()
        return {"tweet_pos_score":tweet_pos_score, "tweet_neg_score": 0 if np.isnan(tweet_neg_score) else tweet_neg_score}
    else:
        return "error"
    

def yt_analysis(yt_username):
    yt_data = yt_stats(yt_username)
    
    if yt_data != "error":
        # Open the JSON file and load the data
        with open(yt_data) as file:
            data = json.load(file)
        
        # Extract the view count and subscriber count
        view_count = data['viewCount']
        subscriber_count = data['subscriberCount']
        
        # Create the yt_stat dictionary
        yt_stat = {
            'views': view_count,
            'subs': subscriber_count
        }
    else:
        yt_stat = "error"
    
    return yt_stat
    
if __name__ == '__main__':
    print(tweet_analysis(input('Enter a brand name: ')))