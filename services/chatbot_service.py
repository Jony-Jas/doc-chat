from fastapi import File, UploadFile
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from services.logger_service import logger
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from tqdm.asyncio import tqdm_asyncio
from dotenv import load_dotenv

import shutil
import re
import os
import time

load_dotenv()
current_file_path = os.path.abspath(__file__)
rootPath = os.path.dirname(os.path.dirname(current_file_path))
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model=os.getenv('GROQ_CHAT_MODEL'))
prompt_template = """Below is an instruction that describes a task, paired with an context that provides further context.
Write a response that appropriately completes the request. If you don't know the answer to a question, please don't share false information. Just say that the question is out of scope.

### Instruction:
You are an electrical engineer and you will answer questions related to electrical engineering from the uploaded pdf context.

### Context:
{context}

### Question:
{question}

### Response:"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
embeddings = NVIDIAEmbeddings(
model=os.getenv("NVIDIA_EMBEDDING_MODEL"), 
api_key=os.getenv("NVIDIA_KEY"), 
truncate="END", 
)

logger.info("Initialized the LLM and Embeddings models.")


class RemoveChainOfThoughtOutputParser(StrOutputParser):
    def parse(self, text: str) -> str:
        # Remove everything between <think> and </think> (including the tags)
        cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        return cleaned_text.strip()
    

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(question: str, file: str):
    try:
        new_db = FAISS.load_local(f"{rootPath}/database/{file}.pdf", embeddings, allow_dangerous_deserialization=True)
    except Exception as file_err:
        logger.error(f"File not found: {str(file_err)}")
        raise Exception("Context not found. Upload the pdf file first.")

    # initialize the RAG Chain
    retriever = new_db.as_retriever()
    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | RemoveChainOfThoughtOutputParser()
    )

    # try:
    query = question
    # This will automatically pass the query to both the retriever and the question slot.
    answer = rag_chain.invoke(query)
    return answer
 
def split_pdf(file_path):
    try:
        loader = PyMuPDFLoader(file_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
        chunks = splitter.split_documents(pages)
        return chunks
    except Exception as file_err:
        logger.error(f"File not found: {str(file_err)}")
        raise Exception("File not found.")
    
async def process_pdf(chunks):
    batch_size = 50  # Matches NVIDIA's default max_batch_size
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    progress_bar = tqdm_asyncio(total=len(texts), desc="Generating embeddings")

    db = FAISS.from_texts(["init"], embeddings)

    try:
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            
            # Get embeddings using NVIDIA's async method
            batch_embeddings = await embeddings.aembed_documents(batch_texts)
            
            # Add to FAISS with metadata
            db.add_embeddings(
                text_embeddings=list(zip(batch_texts, batch_embeddings)),
                metadatas=batch_metadatas
            )
            
            # Update progress
            progress_bar.update(len(batch_texts))

    except Exception as e:
        raise Exception("Error processing batch.")
    finally:
        progress_bar.close()

    return db

async def handle_upload(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        start_time = time.time()
        contents = await file.read()
        file_path = f"{rootPath}/pdfs/{file.filename}"

        # check if the pdf is already processed
        if os.path.exists(f"{file_path}"):
            return "File uploaded successfully.."
        
        with open(file_path, "wb") as gf:
            gf.write(contents)
        logger.info(f"Uploaded file: {file.filename} in {time.time() - start_time} seconds.")


        # split pdf
        start_time = time.time()
        chunks = split_pdf(file_path)
        logger.info(f"Split pdf (len:{len(chunks)}): {file.filename} in {time.time() - start_time} seconds.")

        # process pdf
        start_time = time.time()
        db = await process_pdf(chunks)
        logger.info(f"Processed pdf: {file.filename} in {time.time() - start_time} seconds.")

        db.save_local(f"{rootPath}/database/{file.filename}")

        return "File uploaded successfully."
    
    except Exception as file_err:
        logger.error(f"Error uploading file: {str(file_err)}")
        os.remove(f"{rootPath}/pdfs/{file.filename}")
        raise Exception("Error uploading file.")

def handle_clear_database(filename: str):
    try:
        shutil.rmtree(f"{rootPath}/database/{filename}.pdf")
        pass
    except FileNotFoundError:
        logger.warning(f"Directory {rootPath}/database/{filename} not found, skipping removal.")
    except Exception as e:
        logger.error(f"Error removing directory {rootPath}/database/{filename}: {str(e)}")
        raise Exception("Error removing directory.")

    try:
        os.remove(f"{rootPath}/pdfs/{filename}.pdf")
        logger.info(f"PDF file {filename}.pdf cleared.")
    except FileNotFoundError:
        logger.warning(f"PDF file {rootPath}/pdfs/{filename}.pdf not found, skipping removal.")
    except Exception as e:
        logger.error(f"Error removing file {rootPath}/pdfs/{filename}.pdf: {str(e)}")
        raise Exception("Error removing file.")
    
    return "Cache cleared successfully."

