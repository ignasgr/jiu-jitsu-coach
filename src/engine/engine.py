import os

import openai
from fastapi import FastAPI

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
def myfunc():
    pass