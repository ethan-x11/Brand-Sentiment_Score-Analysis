import os
import csv
from datetime import datetime
import time
import pandas as pd
from analyzer import tweet_analysis, yt_analysis


def create_profile(name, yt_username="", twitter_keyword=""):
    # Check if the file exists
    if not os.path.exists('./data/score'):
        os.makedirs('./data/score')
    scorefile_path = f'./data/score/{name}.csv'
    datetoday = datetime.now().strftime("%d-%m-%Y")
    if not os.path.exists(scorefile_path):
        # Create the file and write the header row
        with open(scorefile_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'name', 'yt_username', 'twitter_keyword', 'score', 'twitter_status', 'tweet_pos_score', 'tweet_neg_score','yt_status',  'yt_sub', 'yt_views','positive_impact','negative_impact'])
            writer.writerow([datetoday, name, yt_username, twitter_keyword, 10, '', 0, 0, '', 0, 0, '', ''])
        return scorefile_path
    else:
        return scorefile_path
    return "Error"


def generate_score(scorefile_path, name):
    results = {}
    results.setdefault('positive_impact', [])
    results.setdefault('negative_impact', [])
    score_csv = pd.read_csv(scorefile_path)
    twitter_status = True
    yt_status = True
    tweet_score = {'tweet_pos_score': 0, 'tweet_neg_score': 0}
    yt_data = {'subs': 0, 'views': 0}


    tweet_score = tweet_analysis(score_csv[score_csv['name'] == name]['twitter_keyword'][0])
    if tweet_score not in ["no_tweet", "error"]:
        twitter_status = True
    else:
        twitter_status = False
    
    yt_data = yt_analysis(score_csv[score_csv['name'] == name]['yt_username'][0])
    if yt_data != "error":
        yt_status = True
    else:
        yt_status = False
        
    print(tweet_score)
    print(yt_data)


    score = score_csv[score_csv['name'] == name]['score'].iloc[-1]
    
    if twitter_status:
            
        tweet_pos_score = tweet_score['tweet_pos_score']
        tweet_neg_score = tweet_score['tweet_neg_score']
        #tweet_score
        if (tweet_pos_score > score_csv[score_csv['name'] == name]['tweet_pos_score'].iloc[-1]):
            score += 1
            reason = "Twitter Positive Posts Increased"
            results.setdefault('positive_impact', []).append(reason)
        elif (tweet_pos_score < score_csv[score_csv['name'] == name]['tweet_pos_score'].iloc[-1]):
            score -= 1
            reason = "Twitter Positive Posts Decreased"
            results.setdefault('negative_impact', []).append(reason)
            
        if (tweet_neg_score > score_csv[score_csv['name'] == name]['tweet_neg_score'].iloc[-1]):
            score -= 1
            reason = "Twitter Negative Posts Increased"
            results.setdefault('negative_impact', []).append(reason)
        elif (tweet_neg_score < score_csv[score_csv['name'] == name]['tweet_neg_score'].iloc[-1]):
            score += 1
            reason = "Twitter Negative Posts Decreased"
            results.setdefault('positive_impact', []).append(reason)
    if yt_status:
        yt_sub = int(yt_data['subs'])
        yt_views = int(yt_data['views'])
        #yt_score
        if (yt_sub > score_csv[score_csv['name'] == name]['yt_sub'].iloc[-1]):
            score += 1
            reason = "YouTube Subscribers Increased"
            results.setdefault('positive_impact', []).append(reason)
        elif (yt_sub < score_csv[score_csv['name'] == name]['yt_sub'].iloc[-1]):
            score -= 1
            reason = "YouTube Subscribers Decreased"
            results.setdefault('negative_impact', []).append(reason)
            
        if (yt_views > score_csv[score_csv['name'] == name]['yt_views'].iloc[-1]):
            score += 1
            reason = "YouTube Views Increased"
            results.setdefault('positive_impact', []).append(reason)
        elif (yt_views < score_csv[score_csv['name'] == name]['yt_views'].iloc[-1]):
            score -= 1
            reason = "YouTube Views Decreased"
            results.setdefault('negative_impact', []).append(reason)
        
    results['score'] = score
    results['twitter_status'] = twitter_status
    results['yt_status'] = yt_status
    
    last_row = score_csv.iloc[-1].copy()
    datetoday = datetime.now().strftime("%d-%m-%Y")
    last_row['date'] = datetoday
    last_row['score'] = score
    last_row['twitter_status'] = twitter_status
    last_row['yt_status'] = yt_status
    if twitter_status:
        last_row['twitter_status'] = "OK"
        last_row['tweet_pos_score'] = tweet_pos_score
        last_row['tweet_neg_score'] = tweet_neg_score
    else:
        last_row['twitter_status'] = "ERROR"
        last_row['tweet_pos_score'] = 0
        last_row['tweet_neg_score'] = 0
    if yt_status:
        last_row['yt_status'] = "OK"
        last_row['yt_sub'] = yt_sub
        last_row['yt_views'] = yt_views
    else:
        last_row['yt_status'] = "ERROR"
        last_row['yt_sub'] = 0
        last_row['yt_views'] = 0
    
    last_row['positive_impact'] = results['positive_impact']
    last_row['negative_impact'] = results['negative_impact']
    
    score_csv = score_csv._append(last_row, ignore_index=True)
    score_csv.to_csv(scorefile_path, index=False)
        
    # print(results)
    return results

def pipeline(name, yt_username = "", twitter_keyword = ""):
    # name = input('Name: ').lower()
    name = name.lower()
    yt_username = yt_username.lower()
    twitter_keyword = twitter_keyword.lower()
    start_time = time.time()
    scorefile_path = f'./data/score/{name}.csv'
    if not os.path.exists(scorefile_path):
        # yt_username = input('Youtube Username: ').lower()
        # twitter_keyword = input('Twitter Keyword: ').lower()
        create_profile(name, yt_username, twitter_keyword)
    else:
        print("File already exists")
    res = generate_score(scorefile_path, name)
    end_time = time.time()
    print(f"Total operational time: {end_time - start_time} seconds")
    return res
    

if __name__ == '__main__':
    name = input('Name: ')
    scorefile_path = f'./data/score/{name}.csv'
    if not os.path.exists(scorefile_path):
        yt_username = input('Youtube Username: ')
        twitter_keyword = input('Twitter Keyword: ')
        print(pipeline(name, yt_username, twitter_keyword))
    else:
        print(pipeline(name))