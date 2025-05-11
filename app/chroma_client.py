import torch
import os

from chromadb import PersistentClient, Settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ChromaDB Configuration
CHROMA_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chromadb"))
default_embegging_model_name = "sentence-transformers/all-mpnet-base-v2"
# model_name = "all-MiniLM-L6-v2"
# model_name = "mxbai‑embed‑large"

def get_embeddings(model_name):
    if torch.backends.mps.is_available():
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name, model_kwargs={'device': 'mps'}
        )
    elif torch.backends.cuda.is_built():
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name, model_kwargs={'device': 'cuda'}
        )
    else:
        embeddings = HuggingFaceEmbeddings(model_name=model_name)

    return embeddings


default_embeddings = get_embeddings(default_embegging_model_name)


def get_client(collection_name, embeddings):
    client = PersistentClient(
        str(os.path.join(CHROMA_BASE_PATH, collection_name)),
        # settings=Settings(chroma_db_impl="duckdb+parquet", persist_directory=".chroma/my-db")
    )
    db = Chroma(
        # persist_directory=os.path.join(CHROMA_BASE_PATH, collection_name),
        client=client,
        embedding_function=embeddings,
        create_collection_if_not_exists=True,
        collection_name=collection_name,
    )
    return db


# chroma_client = get_client('comments', default_embeddings)


def load_data_to_chroma(chroma_client: Chroma, items: list[dict], reset=True):
    documents = [
        Document(page_content=item["text"], metadata=item['metadata']) for item in items if item['text']
    ]
    if reset:
        chroma_client.reset_collection()

    chroma_client.add_documents(documents)
    print(f"Loaded {len(documents)} documents into ChromaDB.")

