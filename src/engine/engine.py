import os
from typing import List, Dict

import openai
from fastapi import FastAPI
from pydantic import BaseModel


openai.api_key = os.environ["OPENAI_API_KEY"]

class ChatHistory(BaseModel):
    history: List[Dict]

class TextInput(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def root():
    return {"Health Status": "OK"}

@app.post("/chat")
def llm_response(payload: ChatHistory) -> dict:

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=payload.history
    )

    return response.choices[0].message

@app.post("/embedding")
def create_embedding(payload: TextInput) -> list:

    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=payload.text
    )

    return response.data[0].embedding