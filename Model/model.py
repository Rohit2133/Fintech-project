from langchain_google_genai import ChatGoogleGenerativeAI # pyright: ignore[reportMissingImports]
from langchain.chains import RetrievalQA # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # type: ignore
from langchain.prompts import PromptTemplate # pyright: ignore[reportMissingImports]  
from langchain_chroma import Chroma # type: ignore
from langchain_huggingface import HuggingFaceEmbeddings   # pyright: ignore[reportMissingImports]
from langchain_google_genai import GoogleGenerativeAIEmbeddings   # pyright: ignore[reportMissingImports]
load_dotenv()


def build_QA_chain():
    
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Load persisted DB
    vectordb = Chroma(
        persist_directory="rag_chroma_db",
        embedding_function=embedding
    )

    # building Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash" , temperature=0.3, max_output_tokens=234)

    # Retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 2})


    # prompt template
    custom_prompt = PromptTemplate(
        template="""You are a helpful financial consultant. 
        Answer the user's question using the retrieved information in a clear and simple way. 
        Do NOT mention words like 'provided text' or 'document'. 
        Question: {question}
        Context: {context}
        Answer:""",
        input_variables=["question", "context"]
    )


    # RAG Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt}
    )

    return qa_chain




