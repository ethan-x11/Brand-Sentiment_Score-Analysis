import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
import datetime

def fetch_tweets(query):
    load_dotenv()

    twitter_data=[]
    payload = {
        'api_key': {os.getenv('SCRAPERAPI_API_KEY')},
        'query': {query},
        'num': '25'
    }
    
    try:
        response = requests.get(
            'https://api.scraperapi.com/structured/twitter/search', params=payload
        )
        data = response.json()
        
        if(data['search_information']['total_results'] <= 0 ):
            return "no_tweet"
        all_tweets = data['organic_results']
        # print(all_tweets)
        for tweet in all_tweets:
            twitter_data.append({
                'position': tweet['position'],
                'title': tweet['title'],
                'snippet': tweet['snippet']
            })

        df = pd.DataFrame(twitter_data)
        datetoday = datetime.datetime.now().strftime("%Y-%m-%d")
        query = query.replace(" ", "_").lower()
        if not os.path.exists('./data/tweets'):
            os.makedirs('./data/tweets')
        file_path = f'./data/tweets/{query}_{datetoday}.csv'
        df.to_csv(file_path, index=False)
        return file_path
    except:
        return "error"

def get_tweets(query):
    print(f"Fetching Tweets about `{query}`...")
    start_time = time.time()
    file_path = fetch_tweets(query.lower())
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return file_path

if __name__ == '__main__':
    query = input('Enter Name of the Brand:')
    print(get_tweets(query))