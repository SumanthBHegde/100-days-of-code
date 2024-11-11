import pandas as pd
import matplotlib.pyplot as plt
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load Dataset
data = pd.read_csv('customer_feedback.csv')

# Data Processing
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = ''.join([c for c in text if c.isalpha() or c.isspace()])
    text = ''.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text

data['Feedback'] = data['Feedback'].apply(preprocess_text)

# -- Sentiment Analysis Model --

# Label Data
data['Sentiment'] = data['Rating'].apply(lambda x: 'Positive' if x >= 4 else 'Negative' if x <= 2 else 'Neutral')

# Split Data
X_train, X_test, y_train, y_test = train_test_split(data['Feedback'], data['Sentiment'], test_size=0.2, random_state=42)

# Vectorization
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)

# Model Training
model = LogisticRegression()
model.fit(X_train_vectorized, y_train)

# Testing and Evaluation
X_test_vectorized = vectorizer.transform(X_test)
accuracy = model.score(X_test_vectorized, y_test)
print("Model Accuracy: ", accuracy)


# -- Custom pipeline and Visualization --

sentiments = data['Sentiment'].value_counts()

# Plot sentiment distribution
plt.figure(figsize=(8,6))
sentiments.plot(kind='pie', autopct='%1.1f%%')
plt.title("Sentiment Distribution of Customer Feedback")
plt.show() 