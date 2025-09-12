from langchain_community.document_loaders import PyPDFLoader # pyright: ignore[reportMissingImports]
from langchain.text_splitter import RecursiveCharacterTextSplitter # pyright: ignore[reportMissingImports]
from langchain_huggingface import HuggingFaceEmbeddings # pyright: ignore[reportMissingImports]
from langchain_chroma import Chroma # pyright: ignore[reportMissingImports]
from langchain_google_genai import GoogleGenerativeAIEmbeddings   # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # type: ignore
load_dotenv()

# List of your PDFs
pdf_files = [
    r"C:\Users\dell\Desktop\Fintech-project\data\data 3.pdf",
    r"C:\Users\dell\Desktop\Fintech-project\data\data 2.pdf",
    r"C:\Users\dell\Desktop\Fintech-project\data\data1.pdf",
    r"C:\Users\dell\Desktop\Fintech-project\data\data 4.pdf",
    r"C:\Users\dell\Desktop\Fintech-project\data\data 5.pdf",
    r"C:\Users\dell\Desktop\Fintech-project\data\data 6.pdf", 
    r"C:\Users\dell\Desktop\Fintech-project\data\data 7.pdf", 
    r"C:\Users\dell\Desktop\Fintech-project\data\data 8.pdf", 
    r"C:\Users\dell\Desktop\Fintech-project\data\data 9.pdf" 
]

docs = []
for pdf in pdf_files:
    loader = PyPDFLoader(pdf)
    docs.extend(loader.load())

# Split into chunks (for embeddings)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = splitter.split_documents(docs)
print(f"Total chunks: {len(documents)}")

# Embeddings
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create and persist the vector database
vectordb = Chroma.from_documents(
    documents,
    embedding = embedding,
    persist_directory="rag_chroma_db"
)

print("✅ All PDFs embedded and stored in rag_chroma_db")