from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import torch
import os

# ChromaDB Configuration
CHROMA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chromadb"))
model_name = "sentence-transformers/all-mpnet-base-v2"
# model_name = "all-MiniLM-L6-v2"
# model_name = "mxbai‑embed‑large"
if not torch.backends.mps.is_available():
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs={'device': 'mps'}
    )
else:
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

chroma_client = Chroma(
    persist_directory=CHROMA_PATH, 
    embedding_function=embeddings,
    create_collection_if_not_exists=True,
    collection_name='comments'
)

chroma_telegram_client = Chroma(
    persist_directory=CHROMA_PATH, 
    embedding_function=embeddings,
    create_collection_if_not_exists=True,
    collection_name='telegram_channel_prian'
)


def get_client(collection_name):
    return Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings,
        create_collection_if_not_exists=True,
        collection_name=collection_name
    )


def load_data_to_chroma(items: list[dict]):
    documents = [
        Document(page_content=item["text"], metadata={}) for item in items
    ]
    if documents:
        # Clear existing data in ChromaDB before loading
        try:
            chroma_client.reset_collection()
            print("Cleared existing ChromaDB collection.")
        except:
            print("No existing ChromaDB collection to clear.")
        
        chroma_client.add_documents(documents)
        print(f"Loaded {len(documents)} documents into ChromaDB.")

        results = chroma_client.similarity_search("tests")
        print(1111, results)
    else:
        print("No documents found in MongoDB to load into ChromaDB.")

