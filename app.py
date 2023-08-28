from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import openai
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from config import MONGO_URI, OPENAI_API_KEY
from routes.analysis_routes import analysis_routes
from routes.main_routes import main_routes
from routes.financial_routes import financial_routes
from routes.analysis_routes import analysis_routes
import os

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)



def get_available_currency_pairs():
    # Aici ar trebui să interoghezi baza de date sau sursa de date pentru a obține lista de perechi valutare
    return ["USD/EUR", "USD/GBP", "USD/JPY"]  # Exemplu de listă

@app.route('/')
def index():
    currency_pairs = get_available_currency_pairs()
    return render_template('index.html', currency_pairs=currency_pairs)

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



@app.route('/get-data-folders')
def get_data_folders():
    base_path = os.path.join(os.getcwd(), 'data')
    currency_pairs = [folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder))]
    return {"currency_pairs": currency_pairs}

@app.route('/get-time-frames/<currency_pair>')
def get_time_frames(currency_pair):
    base_path = os.path.join(os.getcwd(), 'data', currency_pair)
    time_frames = [file.split('.')[0] for file in os.listdir(base_path) if file.endswith('.csv')]
    return {"time_frames": time_frames}
