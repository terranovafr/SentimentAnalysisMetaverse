import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text

# Loading of model and used features in classification
features = pickle.load(open("data/features_selected.pkl", 'rb'))
loaded_model = pickle.load(open("data/classifier.pkl", 'rb'))

print(features)

# Load the dataset to classify
df = pd.DataFrame([])
df = pd.read_csv('data/dataset_post_cleaning.csv')

# Convert a collection of raw documents to a matrix of TF-IDF features.
punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
stop_words = text.ENGLISH_STOP_WORDS.union(punc)
desc = df.tokens_text.values
vectorizer = TfidfVectorizer(stop_words = stop_words)
X = vectorizer.fit_transform(desc)
words = vectorizer.get_feature_names()
df2 = pd.DataFrame(X.toarray(), columns=words)
df2 = df2[features]
print(df2)

# Tweets classification
df["GaussianProcess"] = loaded_model.predict(df2)

df.to_csv('./data/dataset_post_classification.csv', sep=',', index=False)