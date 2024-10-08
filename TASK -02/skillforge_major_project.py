# -*- coding: utf-8 -*-
"""Skillforge MAjor Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15TOHCCqoQ6Yu8J0eimtATDEptXlEcoKk
"""

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import joblib

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Load the dataset from a CSV file (use the provided link)
url = "https://drive.google.com/uc?id=1eslDKi95Pg7BYZKcrXCXPP3KQj_pdnUd"
dataset = pd.read_csv(url)

# Display basic information about the dataset
print(dataset.info())

print(dataset.head())

# Check for missing values
missing_values = dataset.isnull().sum()
print(missing_values)

# Drop rows with missing values (if any)
dataset.dropna(inplace=True)

# Initialize the lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Define a function for text preprocessing
def preprocess_text(text):
    # Tokenize, lowercase, remove punctuation, stopwords, and apply lemmatization
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]  # Remove punctuation
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatize
    return ' '.join(tokens)

# Apply the preprocessing function to the 'tweets' column
dataset['cleaned_tweets'] = dataset['tweets'].apply(preprocess_text)

# Choose one of the vectorizers: CountVectorizer or TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(dataset['cleaned_tweets'])
y = dataset['target']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Multinomial Naive Bayes
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)
nb_predictions = nb_model.predict(X_test)
print("Naive Bayes Classification Report")
print(classification_report(y_test, nb_predictions))

# Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)
print("Logistic Regression Classification Report")
print(classification_report(y_test, lr_predictions))

# K-Nearest Neighbors
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)
knn_predictions = knn_model.predict(X_test)
print("K-Nearest Neighbors Classification Report")
print(classification_report(y_test, knn_predictions))

# Function to plot a normalized confusion matrix
def plot_normalized_confusion_matrix(y_test, y_pred, model_name):
    cm = confusion_matrix(y_test, y_pred)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'{model_name} Normalized Confusion Matrix')
    plt.show()

# Plot normalized confusion matrices
plot_normalized_confusion_matrix(y_test, nb_predictions, "Naive Bayes")

plot_normalized_confusion_matrix(y_test, lr_predictions, "Logistic Regression")

plot_normalized_confusion_matrix(y_test, knn_predictions, "K-Nearest Neighbors")

# Plot the distribution of target labels
plt.figure(figsize=(6,4))
sns.countplot(dataset['target'])
plt.title('Distribution of Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.xticks([0, 1], ['Negative', 'Positive'])
plt.show()

# Word cloud for positive tweets
positive_tweets = ' '.join(dataset[dataset['target'] == 1]['cleaned_tweets'])
wordcloud_positive = WordCloud(width=800, height=400, max_font_size=100, max_words=100, background_color='white').generate(positive_tweets)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Positive Tweets')
plt.show()

# Word cloud for negative tweets
negative_tweets = ' '.join(dataset[dataset['target'] == 0]['cleaned_tweets'])
wordcloud_negative = WordCloud(width=800, height=400, max_font_size=100, max_words=100, background_color='black').generate(negative_tweets)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Negative Tweets')
plt.show()

# Model accuracy scores
model_accuracies = {
    'Multinomial Naive Bayes': nb_model.score(X_test, y_test),
    'Logistic Regression': lr_model.score(X_test, y_test),
    'K-Nearest Neighbors': knn_model.score(X_test, y_test)
}

# Plot model accuracies
plt.figure(figsize=(8,4))
sns.barplot(x=list(model_accuracies.keys()), y=list(model_accuracies.values()))
plt.title('Model Accuracies')
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.show()

# Based on the classification reports and confusion matrices, choose the best-performing model.
best_model = lr_model

# Save the model using joblib
joblib.dump(best_model, 'best_model.pkl')

pip install gensim

from gensim.models import KeyedVectors
GLOVE_DIMENSION = 100

def preprocess_text(text):
    return text.lower()

dataset = pd.read_csv('disaster_tweets_data(DS).csv')
dataset['cleaned_tweets'] = dataset['tweets'].apply(preprocess_text)

# Load GloVe vectors, handling potential dimension mismatches
glove_vectors = KeyedVectors.load_word2vec_format('glove.6B.100d.txt', binary=False, no_header=True, encoding='utf-8', limit=None)

def tweet_to_glove_vector(tweet, glove_vectors):
    words = tweet.split()
    vector = np.zeros(GLOVE_DIMENSION)
    valid_words = 0
    for word in words:
        # Check if the word exists in GloVe
        if word in glove_vectors:
            word_vector = glove_vectors[word]
            # Handle potential dimension mismatches
            if len(word_vector) == GLOVE_DIMENSION:
                vector += word_vector
                valid_words += 1
            else:
                print(f"Warning: Word '{word}' has unexpected dimensionality {len(word_vector)}. Skipping.")
    if valid_words > 0:
        vector /= valid_words
    return vector

# Handle words with unexpected dimensionality
glove_embeddings = np.array([
    tweet_to_glove_vector(tweet, glove_vectors) for tweet in dataset['cleaned_tweets']
])

!pip install transformers
from transformers import BertTokenizer, BertForSequenceClassification

# BERT Model for Classification
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Tokenize and encode sequences in the dataset
def tokenize_function(examples):
    return tokenizer(examples['tweets'].tolist(), padding='max_length', truncation=True)  # Convert to list

# Apply to the entire DataFrame at once
tokenized_data = tokenize_function(dataset)

!pip install streamlit
import streamlit as st

# Streamlit Dashboard for Visualization
st.title("Disaster Tweet Sentiment Analysis")
st.subheader("Explore the data and model predictions")

# Upload CSV file for analysis
uploaded_file = st.file_uploader("disaster_tweets_data(DS).csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())

# Interactive prediction on new tweets
user_input = st.text_area("Enter a tweet for sentiment analysis:")
if st.button("Analyze"):
    cleaned_input = preprocess_text(user_input)
    vector_input = vectorizer.transform([cleaned_input])
    prediction = nb_model.predict(vector_input)
    st.write(f"Predicted Sentiment: {'Positive' if prediction == 1 else 'Negative'}")

print(X_train.shape)  # Should be (n_samples_train, n_features)
print(X_test.shape)   # Should be (n_samples_test, n_features)

df = pd.read_csv('disaster_tweets_data(DS).csv')

# Now you can save the DataFrame to a CSV file
df.to_csv('cleaned_disaster_tweets.csv', index=False)

# Display a final message
print("All steps completed successfully!")