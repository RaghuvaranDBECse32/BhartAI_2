from flask import Flask, render_template, request, jsonify
import os
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk

nltk.download('punkt')

# Load intents from the JSON file
with open("intents.json", "r") as file:
    intents = json.load(file)

# Prepare NLP model
vectorizer = TfidfVectorizer(ngram_range=(1, 4))
clf = LogisticRegression(max_iter=10000)

tags = []
patterns = []

for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

def chatbot_response(text):
    input_data = vectorizer.transform([text])
    tag = clf.predict(input_data)[0]
    for intent in intents:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "Sorry, I didn’t understand that."

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("user_input")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
