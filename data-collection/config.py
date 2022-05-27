import os
from dotenv import load_dotenv
load_dotenv('../.env')
api_key = os.environ.get('API_KEY')
api_secret_key = os.environ.get('API_SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_secret = os.environ.get('ACCESS_SECRET')
bearer_token = os.environ.get('BEARER_TOKEN')