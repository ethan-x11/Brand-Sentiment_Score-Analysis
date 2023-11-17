import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime 
import time

class YTstats:

    def __init__(self, api_key, yt_username):
        self.api_key = api_key
        self.yt_username = yt_username
        self.channel_statistics = None

    def get_channel_statistics(self):
        channel_id = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=id&q={self.yt_username}&type=channel&key={self.api_key}').json()['items'][0]['id']['channelId']

        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={self.api_key}'

        json_url = requests.get(url)
        data = json.loads(json_url.text)

        try:
            data = data["items"][0]["statistics"]
        except:
            data = None

        self.channel_statistics = data
        return data


    def dump(self):
        if self.channel_statistics is None:
            return

        channel_title = self.yt_username
        channel_title = channel_title.replace(" ", "_").lower()

        # generate a json file with all the statistics data of the youtube channel
        if not os.path.exists('./data/ytdata'):
            os.makedirs('./data/ytdata')
        datetoday = datetime.now().strftime("%Y-%m-%d")
        file_path = f'./data/ytdata/{channel_title}_{datetoday}.json'
        with open(file_path, 'w') as f:
            json.dump(self.channel_statistics, f)
        print('file dumped')
        return file_path

def yt_stats(yt_username):
    load_dotenv()
    API_KEY = os.getenv('YT_API_KEY')
    
    print(f"Fetching Youtube data about `{yt_username}`...")
    start_time = time.time()
    try:
        yt = YTstats(API_KEY, yt_username)
        yt.get_channel_statistics()
    except:
        return "error"
    file_path = yt.dump()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return file_path

if __name__ == '__main__':
    yt_username = input('Enter Name of the YT Channel:')
    print(yt_stats(yt_username))