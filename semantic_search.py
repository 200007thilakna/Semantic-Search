from generate_embeddings import generate_embedding
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

# Establish the connection
client = pymongo.MongoClient(uri)

# load the movies collection
db = client.sample_mflix
collection = db.movies


# Use the embeddings
query = "imaginary characters from outer space at war"

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 4,
    "index": "PlotSemanticSearch",
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')