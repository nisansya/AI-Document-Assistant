import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

GROQ_API_KEY= st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

GROQ_MODEL= "openai/gpt-oss-20b"

CHROMA_PATH= "./data/chroma"

COLLECTION_NAME= "document"

TOP_K= 5

FINAL_K= 2