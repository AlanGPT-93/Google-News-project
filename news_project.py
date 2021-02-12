"""
Alan García

How to detect events or products using Google News

"""

### Retrieving Google News

import subprocess


## Parametres

search_topic = "phone"
execution_year = "2018"
start_execution_month = "9"
start_execution_day = "12"
end_execution_month = "9"
end_execution_day = "12"
semester = "S2"
lang = "en"

subprocess.run(['sh','news_extractor.sh', search_topic,execution_year, start_execution_month,\
    start_execution_day, end_execution_month, end_execution_day, semester, lang])


### Preprocess


## Import Stop Words
from nltk.corpus import stopwords
sw_eng = stopwords.words('english') ## English Stop Words
sw_esp = stopwords.words('spanish') ## Spanish Stop Words