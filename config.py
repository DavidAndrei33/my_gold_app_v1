
import os
import secrets
secret_key = secrets.token_hex(16)
SECRET_KEY = secret_key
MONGO_URI = "mongodb://localhost:27017/my_gold_app_db"
OPENAI_API_KEY = "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"  # Inlocuiește cu cheia ta reală
WTF_CSRF_ENABLED = True
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


