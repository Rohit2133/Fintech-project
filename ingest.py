from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader, TextLoader
import pinecone
from config import *

# ---- Pinecone Init ----
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(name=INDEX_NAME, dimension=1536, metric="cosine")

# ---- Load Data ----
loaders = [
    PyPDFLoader("data/financial_goals_article1"),
    TextLoader("data/knowledge.txt")
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

# ---- Chunk Data ----
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# ---- Embeddings ----
embeddings = OpenAIEmbeddings()

# ---- Upload to Pinecone ----
vectorstore = Pinecone.from_documents(chunks, embeddings, index_name=INDEX_NAME)
print("✅ Data uploaded to Pinecone")
