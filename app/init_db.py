from pymongo import MongoClient
from langchain_core.documents import Document
from chroma_client import chroma_client, embeddings
from comments import comments # Import comments

# MongoDB Configuration
MONGODB_URI = "mongodb://localhost:27017/mydb"
client = MongoClient(MONGODB_URI)
db = client.mydb
collection = db.mycollection


def init_database(force = True):
    if force:
        collection.delete_many({}) # Clear existing data
        collection.insert_many(comments)
        print("Database initialized with sample data.")
    else:
        print("Database already initialized.")

def load_data_to_chroma():
    """Loads data from MongoDB to ChromaDB."""
    print("Loading data from MongoDB to ChromaDB...")
    items = list(collection.find({}, {"_id": 0}))
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


if __name__ == "__main__":
    init_database(force=True)
    load_data_to_chroma()
