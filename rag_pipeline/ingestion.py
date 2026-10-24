from langchain_community.document_loaders.pdf import PyPDFLoader
import re
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import uuid
from config import CHROMA_PATH, COLLECTION_NAME
import os
from pypdf import PdfReader
import io

def ingestion_pipeline(uploaded_pdf_files):
    check, status, all_pages= load_uploaded_pdfs(uploaded_pdf_files)

    cleaned_docs= clean_text(all_pages)

    chunked_docs= split_doc(cleaned_docs)

    embeddings= embedding_manager()

    vector_store= VectorStoreManager()
    
    texts= [doc.page_content for doc in chunked_docs]
    embeddings= embeddings.generate_embeddings(texts)
    vector_store.add_documents(chunked_docs, embeddings)

def is_broken_pdf_text(text: str):
  if not text or len(text.strip()) <500:
    return True, "No Extractable text found. PDF might be scanned."
  
  char_per_line = len(re.findall(r'\n\s*[a-zA-Z0-9]\s*\n', text))

  if char_per_line > 50:
    return True, "Text extracted character-by-character (broken font encoding)."
  
  alpha = len(re.findall(r'[a-zA-Z]', text))

  if alpha / max(len(text), 1) < 0.3:
    return True, "Low text quality - mostly symbols/newlines."

  # NEW: check for repeated / overlapped phrases (your LSTM case)
  words = text.split()
  if len(words)< 100:
    return True, f"Too little text extracted ({len(words)} words) - PDF might be scanned"
  
  return False, ""

def load_uploaded_pdfs(uploaded_files):
  if not isinstance(uploaded_files, list):
    uploaded_files= [uploaded_files]
  all_pages= []
  for file in uploaded_files:
    file_bytes= file.getvalue() if hasattr(file, "getvalue") else file
    stream= io.BytesIO(file_bytes)
    pdf_reader= PdfReader(stream)
    full_text= ""
    temp_docs= []
    for i, page in enumerate(pdf_reader.pages):
      text= page.extract_text()
      if text:
        full_text+= text +"\n"
        doc= Document(
          page_content= text,
          metadata= {"source": file.name, "page": i}
        )
        temp_docs.append(doc)

    broken, reason= is_broken_pdf_text(full_text)
    if broken:
      return False, reason, {file.name}
    
    all_pages.extend(temp_docs)
    
  return True, "success", all_pages

def clean_text(docs):
  for doc in docs:
    text= doc.page_content
    text= text.replace("\n", " ")
    text= re.sub(r"\s+", " ", text)
    doc.page_content= text.strip()
  return docs


def split_doc(documents, chunk_size=500, chunk_overlap=50):
  text_splitter= RecursiveCharacterTextSplitter(
      chunk_size= chunk_size,
      chunk_overlap= chunk_overlap
  )

  chunked_docs= text_splitter.split_documents(documents)
  return chunked_docs


class embedding_manager:
  def __init__(self, model_name= 'all-MiniLM-L6-v2'):
    self.model_name= model_name

    self.model= SentenceTransformer(self.model_name)

  def generate_embeddings(self, text):
    embeddings= self.model.encode(text, show_progress_bar= True)
    return embeddings


class VectorStoreManager:
  def __init__(self, persist_directory= CHROMA_PATH, collection_name= COLLECTION_NAME):
    self.persist_directory= persist_directory
    self.collection_name= collection_name
    self.client= None
    self.collection= None
    self._initialize_vector_store()

  def _initialize_vector_store(self):
    self.client= chromadb.PersistentClient(path= self.persist_directory)
    self.collection= self.client.get_or_create_collection(
        name= self.collection_name,
        metadata= {"description" : "vector store collection for pdf embeddings in RAG"}
       )  

  def add_documents(self, documents, embeddings):
    if len(documents) != len(embeddings):
      raise ValueError("number of documents and embeddings does not equal")

    ids=[]
    all_metadata=[]
    documents_content= []
    embedding_list=[]

    for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
      doc_id= f"doc_{uuid.uuid4()}" #doc_a1, doc_a2, doc_a3  uuid will generate new ids
      ids.append(doc_id)
      metadata= dict(doc.metadata)
      metadata["doc_index"]= i
      metadata["content_length"]= len(doc.page_content)
      all_metadata.append(metadata)
      documents_content.append(doc.page_content)
      embedding_list.append(embedding.tolist())

      self.collection.add(
        ids=ids,
        metadatas= all_metadata,
        documents= documents_content,
        embeddings= embedding_list
      )
    
