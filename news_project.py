"""
Alan García

How to detect events or products using Google News

Please read me on https://argarcia1693.medium.com

"""

### Retrieving Google News


## Parameters
import subprocess

search_topic = "phone"  ## "$1"
execution_year = "2018" ## "$2"
start_execution_month = "9" ## "$3"
start_execution_day = "12" ## "$4"
end_execution_month = "9" ## "$5"
end_execution_day = "12" ## "$6"
semester = "S2" ## "$7"
lang = "en"  ## "$8"

subprocess.run(['sh','news_extractor.sh', search_topic, execution_year, start_execution_month,\
    start_execution_day, end_execution_month, end_execution_day, semester, lang])


### Preprocess


## Import Stop Words
from nltk.corpus import stopwords
sw_eng = stopwords.words('english') ## English Stop Words.
sw_esp = stopwords.words('spanish') ## Spanish Stop Words.

## Standardizing text 
def standardized_text(text):
    import re

    text = text.lower() ## convert to lower
    text = re.sub(r'https\S+|@\S+|[^\w\s]|_',' ',text) ## replacing URLs and references with blank space.
    text = re.sub(r'\s+'," ",text).strip()  ## replacing double blank space with a single one.
    
    return text

## Removing stop words
def remove_sw(text): 
    t_ = text.copy()
    stop_words = sw_eng + sw_esp

    for word in text:
        if word in stop_words: 
            t_.remove(word) 
    
    return t_


## Returning preprocessed text
def text_generator(file_name):
    import json

    file_name = f"{file_name}.json"
    
    with open(file_name) as f: ## opening json file
        news_data = json.load(f)

    news_text = []
    for news in news_data:  ## looping through each news

        if len(news["text"]) <2:
            news = news["title"]+" "+news["abstract"]
        else:
            news = news["text"]
        
        news_text.append( " ".join(news for news in remove_sw( standardized_text( news ).split()) )  )
    
    return news_text 


### TF-IDF Weighting


from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

file_name = "phone_en_S2" ## news file's name
corpus = text_generator(file_name) ## preprocessed text
vectorizer = TfidfVectorizer()
tf_idf_matrix = vectorizer.fit_transform(corpus).toarray() ## TF-IDF matrix

tokens_position = np.array( list( vectorizer.vocabulary_.values() ) ) ## tokens' position
tokens = np.array( list( vectorizer.vocabulary_.keys() ) ) ## vocabulary

tfidf_values = np.array([]) 
tfidf_tokens = np.array([])


for tf_idf_vector in  tf_idf_matrix:
    top_10_positions = np.argsort(-1*tf_idf_vector)[:10] ## Top ten TF-IDF by news
    top_10_tfidf = tf_idf_vector[top_10_positions]
    _ = [np.where(tokens_position == tp )[0][0] for tp in top_10_positions]
    top_10_tokens = tokens[_] 
    
    tfidf_values = np.append(tfidf_values, top_10_tfidf)
    tfidf_tokens = np.append(tfidf_tokens, top_10_tokens)

import pandas as pd

most_relevant = pd.DataFrame({"tfidf_tokens":tfidf_tokens, "tfidf_values":tfidf_values} )
most_relevant = most_relevant.groupby("tfidf_tokens").agg("sum" ).sort_values(by = "tfidf_values", ascending = False)
most_relevant = most_relevant.head(70).reset_index() ## The 70 most relevant terms
most_relevant["Freq"] = np.floor(most_relevant["tfidf_values"]*10)
most_relevant = most_relevant.iloc[:,[0,2] ]
most_relevant["Freq"] = most_relevant["Freq"].astype(int)

tfidf_most_relevant_terms = most_relevant.set_index('tfidf_tokens').T.to_dict("records" ) ## Convert DF to a Dict


### Word Cloud

from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(max_font_size = 200, max_words = 50).generate_from_frequencies(tfidf_most_relevant_terms[0] )
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
plt.title("phone_en_S2", weight = 'bold', fontsize = 16, family = "Arial", style = 'italic')
plt.savefig('IphoneXS.png',dpi = 300) ## Saving Word Cloud with High Resolution
plt.show()
