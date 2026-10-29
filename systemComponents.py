# System components: LLM response model, knowledge data model
import os
import json
from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import Text

import torch
from transformers import AutoModel, AutoTokenizer

import faiss

import requests

# Prepare embedding model for upcoming chunks
model_name = 'Snowflake/snowflake-arctic-embed-l-v2.0'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, add_pooling_layer=False)
model.eval()


# Get access token for gigachat model

auth_token = os.getenv("gigachat_auth_key")
url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'ea92a026-bb76-41a1-bc94-479db56ee8f2',
  'Authorization': 'Basic ' + auth_token
}

response = requests.post(url, headers=headers, data=payload, verify = False)

access_token = response.json()["access_token"]



# GigaChat api access

class LLMModel:
    def __init__(self, access_token = access_token):
        self.access_token = access_token

    def generate(self, text):
        url = "https://api.giga.chat/v1/chat/completions"

        payload={
            "model": "GigaChat-2-Max",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }]}
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + self.access_token
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)

        return response.json()["choices"][0]["message"]["content"]
    
# Creating knowledge database
class KnowledgeBase:
    def __init__(self, db_link = "postgresql+psycopg://postgres:luchianN007@localhost:5432/chunks",
                 faiss_index = faiss.IndexFlatL2(1024), embedding_model = model, tokenizer = tokenizer):
        self.db_link = db_link
        self.faiss_index = faiss_index
        self.embedding_model = embedding_model
        self.tokenizer = tokenizer

    def add_chunks(self, documents: List[str]) -> None:
        document_tokens = self.tokenizer(documents, padding=True, truncation=True, return_tensors='pt', max_length=8192)
        document_embeddings = self.embedding_model(**document_tokens)[0][:, 0].detach().numpy()
        self.faiss_index.add(document_embeddings)
        # Adding chunks to database 
        engine = create_engine(self.db_link)
        class Base(DeclarativeBase):
            pass
        class Chunk(Base):
            __tablename__ = "chunks"
            id: Mapped[int] = mapped_column(primary_key=True)
            chunk: Mapped[str] = mapped_column(Text)
        with Session(engine) as session:
            chunks = []
            for idx in range(self.faiss_index.ntotal - len(documents), self.faiss_index.ntotal):
                chunks.append(Chunk(id=idx, chunk = documents[idx - self.faiss_index.ntotal + len(documents)]))
            session.add_all(chunks)
            session.commit()
        print(f"Successfully added {len(documents)} chunks!")

    def retrieve(self, doc, k = 3):
        document_tokens = self.tokenizer([doc], padding=True, truncation=True, return_tensors='pt', max_length=8192)
        document_embedding = self.embedding_model(**document_tokens)[0][:, 0].detach().numpy()
        closest_index = self.faiss_index.search(document_embedding, k = k)[1].tolist()[0]
        # getting data from postgressql database
        engine = create_engine(self.db_link)
        class Base(DeclarativeBase):
            pass
        class Chunk(Base):
            __tablename__ = "chunks"
            id: Mapped[int] = mapped_column(primary_key=True)
            chunk: Mapped[str] = mapped_column(Text)
        retrieved_chunks = []
        with Session(engine) as session:
                for idx in closest_index:
                    stmt = select(Chunk).where(Chunk.id == idx)
                    result = session.execute(stmt).scalars().one_or_none()
                    retrieved_chunks.append(result.chunk)
        return retrieved_chunks

    def save_index(self, path: str):
        faiss.write_index(self.faiss_index, path)
        print("Saved index successfully")