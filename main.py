import os
import ast
import google.generativeai as genai
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from pydantic import BaseModel

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["odoo_swap"]
collection = db["odoo_v1"]

app = FastAPI()

class NLQuery(BaseModel):
    query: str

def get_mongo_query_from_nl(nl_query: str):
    prompt = f"""
    You are a MongoDB expert.

    Each document in the MongoDB collection has:
    - "id": string (user ID)
    - "skills offered": list of strings
    - "skills required": list of strings

    Your task is to convert a user's natural language request into a MongoDB `collection.find(<query>, <projection>)` format.

    Requirements:
    - If multiple skills are mentioned (separated by 'or', 'and', or commas), use `$in` to match any.
    - Only search within the `"skills offered"` field.
    - Always return only the `"id"` field using projection: {{ "id": 1, "_id": 0 }}
    - Output only the Python code: `collection.find(...)` (no explanation, no markdown)

    Example:
    Input: "Find users who are offering Generative AI or Deep Learning"
    Output: collection.find({{"skills offered": {{"$in": ["Generative AI", "Deep Learning"]}}}}, {{"id": 1, "_id": 0}})

    Now convert:
    "{nl_query}"
    """
    response = model.generate_content(prompt)
    try:
        line = response.text.strip().split("collection.find")[1].strip("() \n")
        query_str, projection_str = line.split("},", 1)
        query = ast.literal_eval(query_str + "}")
        projection = ast.literal_eval(projection_str.strip())
        return query, projection
    except Exception as e:
        print("Error parsing Gemini output:", e)
        print("Raw Gemini output:\n", response.text)
        return None, None

@app.post("/search")
def search_users(nl_query: NLQuery):
    query_str = nl_query.query.title()
    query, projection = get_mongo_query_from_nl(query_str)

    if query is None:
        return {"error": "Could not process query"}

    try:
        results = collection.find(query, projection)
        ids = list({doc["id"] for doc in results}) 
        return {"matching_ids": ids}
    except Exception as e:
        return {"error": str(e)}
