# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Load your dataset (replace 'your_dataset.csv' with your actual file)
# Assuming your dataset has two columns: 'text' and 'label'
data = pd.read_csv('./data.csv')

# Split the data into training and testing sets
train_data, test_data, train_labels, test_labels = train_test_split(
    data['text'], data['label'], test_size=0.2, random_state=42
)

# Create a TF-IDF vectorizer to convert text into numerical features
vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust the number of features

# Transform the training and testing text data
train_features = vectorizer.fit_transform(train_data)
test_features = vectorizer.transform(test_data)

# Create a Naive Bayes classifier
classifier = MultinomialNB()

# Train the classifier
classifier.fit(train_features, train_labels)

# Make predictions on the test set
predictions = classifier.predict(test_features)

# Evaluate the model
accuracy = accuracy_score(test_labels, predictions)
print(f"Accuracy: {accuracy:.2f}")

# Display classification report
print("Classification Report:")
print(classification_report(test_labels, predictions))
