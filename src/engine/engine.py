import os
from typing import List

import openai
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    text: str

openai.api_key = os.environ["OPENAI_API_KEY"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def llm_response(history: dict) -> dict:

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history["history"]
    )

    return response.choices[0].message

@app.post("/embedding")
def create_embedding(text: Item) -> list:

    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text.text
    )

    return response.data[0].embedding