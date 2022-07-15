from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
import snscrape.modules.twitter as sntwitter
import pandas as pd

# SCRAPE TWEETS (OR RECOLLECT FROM CSV)
tweets_dataframe = pd.DataFrame([], columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
start_date = datetime.strptime("2021-10-28", '%Y-%m-%d').date()
stop_date = datetime.strptime("2022-06-20", '%Y-%m-%d').date()

while str(start_date) != str(stop_date):
    count = 0
    # setup of the query to scrape
    query_string = "#metaverse " + " since:" + str(start_date - timedelta(days=1)) + " until:" + str(start_date)
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query_string).get_items()):
        # scrape 2000 tweets for each day
        if count == 2000:
            start_date = start_date + timedelta(days=1)
            break

        # duplications filter
        if tweet.content not in tweets_dataframe["Text"].to_list():
            tweet_list = []
            tweet_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
            tmp = pd.DataFrame(tweet_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
            tweets_dataframe = tweets_dataframe.append(tmp)
            count = count + 1

tweets_dataframe.to_csv("snscrape_dataset.csv", sep=",", index=False)

print("done!")
