import string
import botometer
import nltk
nltk.download('stopwords')
from wordcloud import WordCloud
from unidecode import unidecode
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
import pandas as pd
import re

twitter_app_auth = {
                    'consumer_key': "consumer_key",
                    'consumer_secret': "consumer_secret",
                    'access_token': "access_token",
                    'access_token_secret': "access_token_secret"
                   }

botometer_api_url = "https://botometer-pro.p.rapidapi.com"

bom = botometer.Botometer(
                wait_on_ratelimit = True,
                botometer_api_url=botometer_api_url,
                rapidapi_key = "rapidapi_key",
                **twitter_app_auth)

# create the wordcloud
def create_wordcloud(tweet_counter, filename):
    tweet_cloud = WordCloud(background_color="white",
                            width=1000,
                            height=500,
                            relative_scaling=0.5,
                            normalize_plurals=False).generate_from_frequencies(dict(tweet_counter.most_common(100)))
    tweet_cloud.to_file("./{}.png".format(filename))

# remove tweets with the Botometer score over the BOT_THRESHOLD
def remove_bot_tweets(dataframe):
    BOT_THRESHOLD = 0.6
    bot_list = []
    usernames_to_test = dataframe["Username"].drop_duplicates().to_list()
    for screen_name, result in bom.check_accounts_in(usernames_to_test):
        bot_score = max(result['raw_scores']['english']['overall'], result['raw_scores']['universal']['overall'])
        if bot_score > BOT_THRESHOLD:
            bot_list.append(screen_name)
        print("@{0} = {1:.2f}".format(screen_name, bot_score))

    return dataframe[~dataframe['Username'].isin(bot_list)]


def clean_text(text):
    text = str(text)
    # Remove URL
    text = re.sub(r"http\S+", "", text)
    # Remove twitter handlers
    text = re.sub('@[^\s]+', '', text)
    # remove hashtags
    text = re.sub(r'\B#\S+', '', text)
    # Remove all the special characters
    text = ' '.join(re.findall(r'\w+', text))
    # remove all single characters
    text = re.sub(r'\s+[a-zA-Z]\s+', '', text)
    # Substituting multiple spaces with single space
    text = re.sub(r'\s+', ' ', text, flags=re.I)

    # Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)

    # Get rid of some additional punctuation and non-sensical text that was missed the first time around.
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)

    return text

# read the stopwords from a file to remove
def readlines():
    stopwords_file = open('stopwords.txt', 'r')
    lines = stopwords_file.readlines()
    # Strips the newline character
    stopwords = []
    for line in lines:
        stopwords.append(line.strip())
    return stopwords

# read the raw dataset
tweet_list = []
tweets_dataframe = pd.DataFrame([])
tweets_dataframe = pd.read_csv('data/raw_dataset.csv')

# REMOVE TWEETS FROM BOTS
#tweets_dataframe = remove_bot_tweets(tweets_dataframe)

# NLP(TOKENIZATION, NORMALIZATION, FILTERING, STEMMING, DESTEMMING)
STOPWORDS_EN = set(stopwords.words("english"))
file_stopwords = readlines()
STOPWORDS_EN = STOPWORDS_EN.union(set(file_stopwords))

STEMMER_EN = PorterStemmer()

formatted_tweets = tweets_dataframe.to_dict('records')

merged_splitted = []
merged_normalized = []
merged_filtered = []
merged_stemmed = []
merged_destemmed = []

for i in formatted_tweets:
    # cleaning
    i["Text_Cleaned"] = clean_text(i["Text"])
    # tokenization
    tokens = re.split('\W+', i["Text_Cleaned"], flags=re.UNICODE)
    # normalization
    normalized = [unidecode(t.lower()) for t in tokens]
    # filtering
    filtered = [t for t in normalized if len(t) >= 3 and t not in STOPWORDS_EN]
    # stemming
    stemmed = [STEMMER_EN.stem(t) for t in filtered]
    # destemming
    stem_mapping = {}
    for f in filtered:
        stemmed_f = STEMMER_EN.stem(f)
        if stemmed_f not in stem_mapping:
            stem_mapping[stemmed_f] = Counter()
        stem_mapping[stemmed_f].update([f])

    i["tokens"] = [stem_mapping[t].most_common(1)[0][0] for t in stemmed]
    i["tokens_text"] = " ".join(i["tokens"])

    merged_splitted = merged_splitted + tokens
    merged_normalized = merged_normalized + normalized
    merged_filtered = merged_filtered + filtered
    merged_stemmed = merged_stemmed + stemmed
    merged_destemmed = merged_destemmed + i["tokens"]

# wordcloud generation of each step of NLP process
create_wordcloud(Counter(merged_splitted), "wordcloud_1")
create_wordcloud(Counter(merged_normalized), "wordcloud_2")
create_wordcloud(Counter(merged_filtered), "wordcloud_3")
create_wordcloud(Counter(merged_stemmed), "wordcloud_4")
create_wordcloud(Counter(merged_destemmed), "wordcloud_5")

formatted_tweets = pd.DataFrame(formatted_tweets)
formatted_tweets = formatted_tweets[formatted_tweets['tokens'].map(len) != 0]
formatted_tweets.to_csv('dataset_post_cleaning.csv', sep=',', index=False)

