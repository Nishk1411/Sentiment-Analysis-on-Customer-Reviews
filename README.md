# Sentiment Analysis with LSTM and GRU models
This project aims at building a Machine Learning model for Sentiment Analysis task using LSTM and GRU 

## Data scraping for training
Used python and selenium to build a web-scrapper to collect product reviews in their original form. Collected 8000+ reviews.
Utilized amazoncaptcha to bypass captcha page of amazon.

```python
from amazoncaptcha import AmazonCaptcha
``` 

You can easily install amazoncaptcha using following pip command in the notebook

```notebook
!pip install amazoncaptcha
```

Saved reviews in a ```.csv``` format.

## Data Labeling
Labeled the reviews as positive or negative using transformer pipeline for sentiment analysis task to ensure accurate labeling of reviews.

```python
from transformers import pipeline
model = pipeline('sentiment-analysis')
```

## Preprocessing and Training
Employed NLP techniques such as tokenization, stemming and stopwords removal to preprocess data for training.
Used the training data to train LSTM model with 92% accuracy and GRU model with 91% accuracy on test data.
