from flask import Flask, request, jsonify, render_template
import json
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2

# Specify the NLTK data path
nltk.data.path.append('./nltk_data')

# Download NLTK data
nltk.download('punkt', download_dir='./nltk_data')
nltk.download('stopwords', download_dir='./nltk_data')
nltk.download('wordnet', download_dir='./nltk_data')

app = Flask(__name__)

# Load corpus from PDF
def load_corpus(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + ' '
        return text

corpus = load_corpus('Corpus.pdf')

# Preprocessing steps
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([corpus])

# Question-Answering model
qa_pipeline = pipeline("question-answering")

# Chatbot response
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    print(f"User Input: {user_input}")  # Log user input
    question = preprocess_text(user_input)
    print(f"Preprocessed Question: {question}")  # Log preprocessed question
    answer = qa_pipeline(question=question, context=corpus)
    print(f"Answer: {answer}")  # Log answer
    return jsonify({'response': answer['answer']})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
