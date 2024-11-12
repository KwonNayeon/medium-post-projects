# -*- coding: utf-8 -*-
# Crawling Naver blogs related to Taiwan travel and performing text analysis


*   Crawling Naver blogs
*   Text analysis

## Crawling Naver blogs

## Install necessary packages
"""

# Install necessary packages
!apt-get update
!apt-get install -y chromium-browser chromium-chromedriver python3-selenium
!pip install selenium webdriver-manager beautifulsoup4

"""## Basic setup and prepare the webdriver"""

# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import re
import os
import sys
import urllib.request
import json
import pandas as pd

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Set up the webdriver
driver = webdriver.Chrome(options=chrome_options)

"""### Test the Chrome driver connection"""

# Test code
try:
    # Access Google
    driver.get('https://www.google.com')
    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)
    print("Setup complete! Selenium is working properly.")

except Exception as e:
    print("Error occurred:", e)

finally:
    driver.quit()

"""## Naver API to Get Blog URLs Related to a Specific Search Keyword"""

# Input Naver API key
client_id = ''  # The user must input their own client ID.
client_secret = ''  # The user must input their own client secret.

# Initialize lists for storing Naver blog data
naver_urls = []
postdate = []
titles = []

# Set default keyword
default_keyword = "대만 여행"

# Input search keyword (default: '대만 여행 = Taiwan travel')
keyword = input(f"Enter the keyword to search (default: {default_keyword}): ")
if not keyword:  # Use default if no input
    keyword = default_keyword
encText = urllib.parse.quote(keyword)

# Input the page number to stop crawling
end = input("\nEnter the page number to stop crawling. (default: 1, maximum: 100):")
if end == "":
    end = 1
else:
    end = int(end)
print(f"\nCrawling will proceed from page 1 to {end}.")

# Input number of pages to retrieve at once
display = input("\nEnter the number of pages to retrieve at once. (default: 10, maximum: 100):")
if display == "":
    display = 10
else:
    display = int(display)
print(f"\nNumber of pages to retrieve at once: {display} pages")

for start in range(end):
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&start={start+1}&display={display+1}"  # JSON response
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))['items']
        for row in data:
            if 'blog.naver' in row['link']:
                naver_urls.append(row['link'])
                postdate.append(row['postdate'])
                title = row['title']
                # Remove HTML tags from title
                pattern1 = '<[^>]*>'
                title = re.sub(pattern=pattern1, repl='', string=title)
                titles.append(title)
        time.sleep(2)
    else:
        print("Error Code:", rescode)

# Extract article content and titles from Naver

# Prevent ConnectionError
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

contents = []
comments_texts = []

try:
    for i in naver_urls:
        print(i)
        driver.get(i)
        time.sleep(5)  # You can adjust the wait time here

        iframe = driver.find_element(By.ID, "mainFrame")  # Locate the element with id 'mainFrame' -> iframe
        driver.switch_to.frame(iframe)  # Switch to the iframe that contains the desired HTML content

        source = driver.page_source
        html = BeautifulSoup(source, "html.parser")

        # Extract article content
        content = html.select("div.se-main-container")
        content = ''.join(str(content))  # Combine the list into a single string

        # Remove HTML tags and clean up the content
        content = re.sub(pattern=pattern1, repl='', string=content)
        pattern2 = """[\n\n\n\n\n// Function added to bypass flash error\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')
        content = content.replace('\n', '')
        content = content.replace('\u200b', '')
        contents.append(content)

    # Create a DataFrame and save to CSV
    news_df = pd.DataFrame({'title': titles, 'content': contents, 'date': postdate})
    news_df.to_csv('taiwan_travel_blog', index=False, encoding='utf-8-sig')

except Exception as e:
    contents.append('error')
    news_df = pd.DataFrame({'title': titles, 'content': contents, 'date': postdate})
    news_df.to_csv('taiwan_travel_blog', index=False, encoding='utf-8-sig')
    print(f"An error occurred: {e}")

"""## Text Analysis

## Read data
"""

!pip install konlpy

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

import pandas as pd
from io import BytesIO
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer

# File path with proper extension (e.g., .csv)
file_path = '/content/drive/MyDrive/taiwan_travel_blog'

# Read the binary data and convert it to a pandas DataFrame
with open(file_path, 'rb') as file:
    binary_data = file.read()

# Read binary data as CSV
df = pd.read_csv(BytesIO(binary_data))

# Display the first 5 rows of the DataFrame
print(df.head())

"""## Pre-processing"""

# Initialize Okt morphological analyzer
okt = Okt()

# 1. Set file path for stopwords (Korean stopwords)
stopwords_path = '/content/drive/MyDrive/stopwords-ko.txt'

# 2. Load Korean stopwords
with open(stopwords_path, 'r', encoding='utf-8') as file:
    stop_words_ko = file.read().splitlines()  # Treat each line as a stopword

# 3. Additional English stopwords
english_stopwords = ['pzp', 'pc', 'p', 'hdp', 'hd', 'space', 'pc', 'brand',
                     'pc brand', 'height', 'brand', 'playback', 'brand playback',
                     'width', 'x', 'poster loaded', 'background size', 'px px',
                     'ui icon', 'size contain', 'px', 'twd', 'd', 'background']

# 3-2. Additional Korean stopwords
kor_stopwords = ['재생', '자동', '속도', '해상도', '전체화면', '아이콘', '실시간', '0초',
                 '도', '는', '은', '하는', '있는', '하고', '인데', '에는', '때문', '사용',
                 '이용', '서', '해서', '입니다', '시', '볼']

# 4. Combine Korean stopwords and English stopwords
stop_words = stop_words_ko + english_stopwords + kor_stopwords

# Dataframe preprocessing
# 1. Remove HTML tags
df['cleaned_text'] = df['content'].str.replace(r'<[^>]*>', '', regex=True)

# 2. Convert text to lowercase (for English as well)
df['cleaned_text'] = df['cleaned_text'].str.lower()

# 3. Remove stopwords (both Korean and English)
df['cleaned_text'] = df['cleaned_text'].apply(lambda x: ' '.join([word for word in okt.morphs(x) if word not in stop_words]))

# 4. Morphological analysis (analyze each word)
df['cleaned_text'] = df['cleaned_text'].apply(lambda x: ' '.join(okt.morphs(x)))

# 5. Keep only texts with more than 3 words
df = df[df['cleaned_text'].str.split().str.len() > 2]

# 6. Remove special characters
df['cleaned_text'] = df['cleaned_text'].str.replace(r'[^가-힣a-zA-Z0-9\s]', '', regex=True)

# 7. Tokenize the text into words
df['tokens'] = df['cleaned_text'].apply(lambda x: okt.morphs(x))

# Check the result
print(df[['content', 'cleaned_text']].head())

"""## Text analysis


1.   Analyzing frequently appearing keywords (TF-IDF)
2.   Sentiment analysis
3.   Topic modeling (LDA)
4.   Generating word cloud




"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from datetime import datetime
import nltk

# Download NLTK Vader lexicon
nltk.download('vader_lexicon')

# Install Korean font (for use in Colab)
!apt-get install -y fonts-nanum

# Specify the path to the Nanum Gothic font
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

# 1. Analyzing frequently appearing keywords (TF-IDF)
vectorizer = TfidfVectorizer(max_features=10, stop_words=stop_words)  # Apply stop words list
X = vectorizer.fit_transform(df['cleaned_text'])
keywords = vectorizer.get_feature_names_out()

print("Most important keywords:", keywords)

# 2. Sentiment analysis
analyzer = SentimentIntensityAnalyzer()
df['sentiment_score'] = df['cleaned_text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
df['sentiment_label'] = df['sentiment_score'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))

print("\nSentiment analysis results:")
print(df[['cleaned_text', 'sentiment_label']].head())

# 3. Topic modeling (LDA)
vectorizer = CountVectorizer(stop_words=stop_words)  # Apply stop words list
X = vectorizer.fit_transform(df['cleaned_text'])

lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X)

print("\nTopic modeling results:")
for i, topic in enumerate(lda.components_):
    print(f"Topic {i + 1}:")
    print([vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-10:]])

# 4. Generating word cloud
# Set path to Korean font
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

# Generate word cloud
wordcloud = WordCloud(
    font_path=font_path,  # Path to Korean font
    width=800,            # Image width
    height=400,           # Image height
    background_color='white',  # Set background color to white
    colormap='Blues',         # Use calm color palette
    max_words=100,           # Limit the maximum number of words
    min_font_size=10,        # Set minimum font size
    collocations=False       # Disable word collocations (to prevent excessive combinations of words)
).generate(' '.join(df['cleaned_text']))

# Visualize word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Remove axis
plt.show()

# Save the word cloud image
output_path = '/content/wordcloud_taiwan.png'  # Specify the path where you want to save the image
wordcloud.to_file(output_path)

# If you want to use plt.savefig(), you can also do this:
# plt.savefig(output_path, format='png', dpi=300)  # Save as PNG image

print(f"Word cloud image saved to: {output_path}")