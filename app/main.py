from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Dict
from langchain_core.documents import Document # Keep Document as it's used in the query function signature if needed later
from app.chroma_client import chroma_client
from langchain_ollama import ChatOllama

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

# MongoDB Configuration
MONGODB_URI = "mongodb://127.0.0.1:27017/mydb"  # Use the service name 'mongo'
client = MongoClient(MONGODB_URI)
db = client.mydb
collection = db.mycollection


llm_model = ChatOllama(
    model="llama3.2:3b",
)

GENERATE_PROMPT_TEMPLATE = """
You are an AI assistant analyzing Fisheye/Stash code review comments.
Based solely on the following comments provided as context, please answer the user's question.
If the comments don't provide enough information, state that.

Context Comments:
{context_comments}

User Question: {query}

Answer:
"""

EXPANTION_PROMPT_TEMPLATE = """You are an AI language model assistant.
Your task is to generate {expand_to_n}
different versions of the given user question to retrieve relevant documents from a vector
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search.
Provide these alternative questions seperated by '{separator}'.
Original question: {question}"""


class RequestQuery(BaseModel):
    query: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items", response_model=List[Dict])
async def read_items():
    items = list(collection.find({}, {"_id": 0}))  # Exclude _id field
    return items

@app.post("/query")
async def query_data(request: RequestQuery):
    augment_prompt = AUGMENT_PROMPT_TEMPLATE.format(
        query=request.query
    )
    additional_questions = llm_model.invoke(generate_prompt)
    print("New questions:", additional_questions)

    results = chroma_client.similarity_search(request.query)

    # Extract comment text from results
    context_comments = "\n\n --- \n\n".join([doc.page_content for doc in results])

    print(f"Simular content: {context_comments}")

    # Format the prompt using the template and context
    generate_prompt = GENERATE_PROMPT_TEMPLATE.format(
        context_comments=context_comments,
        user_query=request.query
    )

    try:
        answer = llm_model.invoke(generate_prompt)
        # end_time = time.time()
        # request_time = end_time - start_time
        print(f"Ollama response: {answer}")
        return {"answer": answer.content, "context": [doc.page_content for doc in results]}
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return {"error": f"Could not get response from Ollama: {e}"}