FROM python:3.10

WORKDIR /src/engine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY engine.py .

CMD ["uvicorn", "engine:app", "--host", "0.0.0.0", "--port", "80"]