# SentimentAnalysisMetaverse
Sentiment analysis can be used to understand the opinions and concerns of customers and receive their feedback. Using our tool, companies can understand key actions of competitors, already entered in the Metaverse, that obtained positive or negative sentiment.

## Project Structure
The project contains many Python files and Jupyter notebooks organized in folders describing the branch of Machine learning techniques they refer to. 
- Classification/ contains the source code used to perform the classifiers' comparison, as well as the .pkl file of the final classifier
- Clustering/ contains the source code of the clustering techniques used for topic modeling. 
- SentimentAnalysis/ contains the source code of the techniques used to perform sentiment analysis on the tweets.
- TopicModeling/ contains the source code of the techniques used for topic modeling.
- data/ contains the dataset used during the different steps, as well as some results obtained

## Data Analysis
The data used in this study has been gathered using Twitter's API and the snscrape tool.<br>
Botometer has been used as a tool for bot detection, removing tweets whose bot probability was above a certain threshold.<br>
A pipeline of NLP steps has been then performed: 
<ul>
 <li>Data Cleaning</li>
 <li>Tokenization</li>
 <li>Normalization</li>
 <li>Filtering</li>
  <li>Stemming</li>
</ul>
Subsequently, sentiment analysis has been performed using different tools, such as TextBlob, Sentiment Intensity Analyzer (SIA), and a trained classifier chosen comparing different Machine learning techniques using a K-Fold Cross Validation.<br>
The models have been combined using an ensemble learning approach.
<br>
The tweets posted during the days that showed high positive sentiment or high negative sentiment were analyzed using topic modeling and clustering techniques.
Different results obtained were compared with well-known news information during these days related to the Metaverse topic, proving the ability of the algorithm to detect the sentiment and the reason behind it.<br>
<p align="center">
  <img width="597" alt="Screenshot 2023-07-05 alle 20 53 56" src="https://github.com/terranovaa/SentimentAnalysisMetaverse/assets/61695945/7a1aa277-c07d-4381-9624-4b1beaf0a899">
</p>
More information can be found on the presentation and documentation files.
