import os
import pymongo
import requests
from dotenv import load_dotenv, dotenv_values
import urllib.parse

load_dotenv()
username = urllib.parse.quote_plus(os.getenv('USER_NAME'))
password = urllib.parse.quote_plus(os.getenv('PASSWORD'))

# Construct the MongoDB URI with escaped username and password
uri = f"mongodb+srv://{username}:{password}@cluster0.11fmfak.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
print(uri)
# Establish the connection
client = pymongo.MongoClient(uri)

# load the movies collection
db = client.sample_mflix
collection = db.movies

# using a huggingface inference API : all-MiniLM-L6-v2
hf_token = os.getenv('HF_TOKEN')
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


# Set up the embedding creating function
def generate_embedding(text: str) -> list[float]:

  response = requests.post(
    embedding_url,
    headers={"Authorization": f"Bearer {hf_token}"},
    json={"inputs": text})

  if response.status_code != 200:
    raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

  return response.json()

# create vector embeddings for the data
for doc in collection.find({'plot':{"$exists": True}}).limit(21349):
  doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
  collection.replace_one({'_id': doc['_id']}, doc)



