# This python script generates the WordClouds of each clustering results
# provided in csv in the specified folder

import os
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import re

# create the wordcloud
def create_wordcloud(tweet_counter, filename):
    tweet_cloud = WordCloud(background_color="white",
                            width=1000,
                            height=500,
                            relative_scaling=0.5,
                            normalize_plurals=False).generate_from_frequencies(dict(tweet_counter.most_common(100)))
    tweet_cloud.to_file("./{}.png".format(filename))

# Get the list of all files and directories
path = "./"

token_list = []
tweets_dataframe = pd.DataFrame([])
for x in os.listdir(path):
    if x.endswith(".csv"):
        # Prints only text file present in My Folder
        tweets_dataframe = pd.read_csv(path + "//" + x)
        tweets_dataframe = tweets_dataframe[tweets_dataframe["Class"] != -1]
        print(tweets_dataframe)
        for i in range(tweets_dataframe["Class"].max()+1):
            rows = tweets_dataframe.loc[tweets_dataframe["Class"] == i]
            text = ""
            for j in rows["Text"]:
                text = text + j
            tokens = re.split('\W+', text, flags=re.UNICODE)
            size = len(x)
            create_wordcloud(Counter(tokens), "wordcloud_" + str(i) + "_" + x[: size-3])


