"""
Alan García

How to detect events or products using Google News

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

preprocessed_text = text_generator("phone_en_S2")

print(preprocessed_text[:2] )