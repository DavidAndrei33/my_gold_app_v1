from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import openai
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from config import MONGO_URI, OPENAI_API_KEY
from routes.analysis_routes import analysis_routes
from routes.main_routes import main_routes
from routes.financial_routes import financial_routes
from routes.analysis_routes import analysis_routes


app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Load pre-trained model and tokenizer once for distilgpt2
tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
model = GPT2LMHeadModel.from_pretrained("distilgpt2")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    message = request.json.get('message')

    # Encode input message and generate response
    input_ids = tokenizer.encode(message, return_tensors='pt')
    output = model.generate(
        input_ids, 
        max_length=150, 
        num_return_sequences=1,
        temperature=0.7,  # Adjust this as needed
        top_k=40,        # Adjust this as needed
        top_p=0.92,      # Adjust this as needed
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True
    )
    response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    return jsonify(response=response)

app.register_blueprint(main_routes)
app.register_blueprint(analysis_routes)
app.register_blueprint(financial_routes, url_prefix='/financial')
if __name__ == '__main__':
    app.run(debug=True)
