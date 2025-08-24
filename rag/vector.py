from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import Document
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv
import pandas as pd
import os

import streamlit as st
# ✅ Load environment variables
load_dotenv("config/.env")
OPENAI_API_KEY = st.secrets["openai_api_key"]

# ✅ Load JEEBench dataset as Documents
def load_jeebench_documents():
    import json
    with open("data/test.json", "rb") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    documents = []
    for i, row in df.iterrows():
        q = row["question"]
        a = row["gold"]
        text = f"Q: {q}\nA: {a}"
        doc = Document(text=text, metadata={"source": "jee_bench", "index": i})
        documents.append(doc)
    return documents

# ✅ Build the vector index using Qdrant
def build_vector_index():
    documents = load_jeebench_documents()

    node_parser = SimpleNodeParser()
    nodes = node_parser.get_nodes_from_documents(documents)

    qdrant_client = QdrantClient(host="localhost", port=6333)
    collection_name = "math_agent"

    if not qdrant_client.collection_exists(collection_name=collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

    vector_store = QdrantVectorStore(client=qdrant_client, collection_name=collection_name)
    embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(nodes=nodes, embed_model=embed_model, storage_context=storage_context)
    index.storage_context.persist()

    print("✅ Qdrant vector index built and saved successfully.")

if __name__ == "__main__":
    build_vector_index()
