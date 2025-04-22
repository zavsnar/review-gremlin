from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import torch

# ChromaDB Configuration
CHROMA_PATH = "chromadb"
model_name = "sentence-transformers/all-mpnet-base-v2"
# model_name = "all-MiniLM-L6-v2"
# model_name = "mxbai‑embed‑large"
if not torch.backends.mps.is_available():
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={'device': 'mps'})
else:
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

chroma_client = Chroma(
    persist_directory=CHROMA_PATH, 
    embedding_function=embeddings,
    create_collection_if_not_exists=True,
    collection_name='comments'
)