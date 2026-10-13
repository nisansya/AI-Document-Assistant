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

def ingestion_pipeline(uploaded_pdf_files):
    all_pages= load_uploaded_pdfs(uploaded_pdf_files)

    cleaned_docs= clean_text(all_pages)

    chunked_docs= split_doc(cleaned_docs)

    embeddings= embedding_manager()

    vector_store= VectorStoreManager()
    
    texts= [doc.page_content for doc in chunked_docs]
    embeddings= embeddings.generate_embeddings(texts)
    vector_store.add_documents(chunked_docs, embeddings)

def load_uploaded_pdfs(uploaded_files):
  all_pages= []
  for file in uploaded_files:
    pdf_reader= PdfReader(file)
    for i, page in enumerate(pdf_reader.pages):
      text= page.extract_text()
      if text:
        doc= Document(
          page_content= text,
          metadata= {"source": file.name, "page": i}
        )
        all_pages.append(doc)
    
  return all_pages
  # for file in uploaded_files:
  #   if file.name.lower().endswith(".pdf"):
  #     file_path= os.path.join(file.name)
  #     pdf_loader= PyPDFLoader(file)
  #     document=pdf_loader.load()
  #     all_pages.extend(document)

  #   else:
  #     return False
  # print(document)
  # print(all_pages)

  # return all_pages


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
    
