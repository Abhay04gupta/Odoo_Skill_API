import os
import re
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
    - Always return all the fields like "name", "id", "city", "availability"` field using projection: {{ "id": 1, "_id": 0, "name":1,"city":1, "availability":1 }}
    - Output only the Python code: `collection.find(...)` (no explanation, no markdown)

    Now convert:
    "{nl_query}"
    """
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    try:
        # Extract content inside collection.find(...)
        match = re.search(r"collection\.find\((\{.*\}),\s*(\{.*\})\)", raw_text, re.DOTALL)
        if not match:
            raise ValueError("Couldn't find valid collection.find pattern")

        query_str = match.group(1)
        projection_str = match.group(2)

        query = ast.literal_eval(query_str)
        projection = ast.literal_eval(projection_str)

        return query, projection
    except Exception as e:
        print("Error parsing Gemini output:", e)
        print("Raw Gemini output:\n", raw_text)
        return None, None


@app.post("/search")
def search_users(nl_query: NLQuery):
    query_str = nl_query.query.title()
    query, projection = get_mongo_query_from_nl(query_str)

    if query is None:
        return {"error": "Could not process query"}

    try:
        response = collection.find(query, projection)
        results=[]
        for data in response:
            results.append(data)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
