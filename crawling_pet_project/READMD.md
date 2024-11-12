# Project: Web Scraping and Text Analysis of Travel Trends on Blogs

This project focuses on web scraping Naver blogs related to Taiwan travel and performing text analysis to uncover insights into travel trends. The project performs sentiment analysis, keyword extraction, and topic modeling (LDA) on the extracted blog data, along with generating word clouds. The accompanying Medium post [**Web Scraping and Text Analysis of Travel Trends on Blogs**](https://nayeonkwonds.medium.com/web-scraping-and-text-analysis-of-travel-trends-on-blogs-e83a453d34ed) provides further context on the approach and results.

## Files
1. **`code/crawling_pet_project.py`**  
   Python script for web scraping Naver blogs related to Taiwan travel, performing text analysis (sentiment analysis, keyword extraction, topic modeling), and generating word clouds.

## API Key
Please note that the **Naver API key** has been omitted for privacy and security reasons. You will need to provide your own Naver API key to run the web scraping script. You can obtain the API key by following the instructions on the [Naver Developers website](https://developers.naver.com/).

In the code, replace the following placeholders with your own API key:

```python
client_id = ''  # Your Naver API Client ID
client_secret = ''  # Your Naver API Client Secret
```

## Requirements
Make sure you have the following Python libraries installed:

```bash
# Install necessary packages
!apt-get update
!apt-get install -y chromium-browser chromium-chromedriver python3-selenium
!pip install selenium webdriver-manager beautifulsoup4
```

Then, import the required libraries in your script:

```python
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
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime
import nltk
```

## Data Sources and Acknowledgments
- **Naver Developer API** for web scraping: [Naver Developers website](https://developers.naver.com/)  
- Python-based Naver blog crawling tutorial by dev-woo: [link](https://developer-woo.tistory.com/60#google_vignette)  
- The project uses the **stopwords-ko.txt** from [spikeekips' Gist on GitHub](https://gist.github.com/spikeekips/40eea22ef4a89f629abd87eed535ac6a)

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/KwonNayeon/medium-post-projects/blob/main/LICENSE) file for more details.