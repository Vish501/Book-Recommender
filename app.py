import os
import pandas as pd
import numpy as np

import gradio as gr

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Loading environment variables from .env file
load_dotenv()

# Setting environment variable `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION` due to issues with importing 'langchain_chroma'
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Changing directory to main directory for data access
working_directory = os.getenv("WORKING_DIRECTORY")
os.chdir(working_directory)

# Loading in dataset
books = pd.read_csv("data/books_emotions_and_thumbnail.csv")

# Manually constructing LangChain Document object
document_object = [
    Document(
        page_content=row["description"],
        metadata={"source": str(row["isbn13"])}
    )
    for _, row in books.iterrows()
]

# Initialzing the embeddings object
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001" )

# Constructing the database
db_books = Chroma.from_documents(document_object, embedding=embeddings)

