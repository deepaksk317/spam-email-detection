import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
df = pd.read_csv('phishing_email_dataset.csv')

# Split data into features and labels
X = df['email_text']
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create a model
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Save the vectorizer and model
with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

with open('phishing_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

# Evaluate the model
accuracy = model.score(X_test_vec, y_test)
print(f"Model accuracy: {accuracy * 100:.2f}%")
