from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from config import *

# ---- Pinecone Init ----
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# ---- Embeddings ----
embeddings = OpenAIEmbeddings()

# ---- Load VectorStore ----
vectorstore = Pinecone.from_existing_index(INDEX_NAME, embeddings)

# ---- Query ----
query = "What is LangChain?"
results = vectorstore.similarity_search(query, k=3)

print("🔍 Query:", query)
for doc in results:
    print("➡️", doc.page_content[:200])  # preview
