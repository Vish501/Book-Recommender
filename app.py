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

# Setting variables for dropdown menus
category_labels = ["All"] + sorted((books["base_categories"].unique()))
emotion_labels = ["All"] + sorted(["Anger", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Neutral"])

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

# Function to retrieve all the recommendations as a dataframe
# Inputs - Dataset, Chroma vector database, query, number of recommandations
# Outputs - List of Books as a df
def retrieve_semantic_recommendations(books: pd.DataFrame, db_books: Chroma, query: str, no_of_recc: int = 50) -> pd.DataFrame:
    response_books = db_books.similarity_search(query, k=no_of_recc)
    isbn_list = [int(doc_object.metadata["source"]) for doc_object in response_books]
    return books[books["isbn13"].isin(isbn_list)]

# Function to recommandation books
# Inputs - Dataset, Chroma vector database, query, category, tone, name, initial top_k, final top_k
# Outputs - Ordered list of books as df based on filters
def recommand_books(books: pd.DataFrame, db_books: Chroma, query: str, category: str, tone: str, name: str, inital_no_of_recc: int = 50, final_no_of_recc: int = 24):
    pass

# Main Block that renders the app dashboard
with gr.Blocks(theme=gr.themes.Glass()) as dashbaord:
    gr.Markdown("# Book Recommender")

    # Filters for book recommandations
    with gr.Row():
        name_filter = ...
        query_filter = ...
        category_filter = ...
        emotion_filter = ...
        submit_button = ...
    
    # Recommandations using inputs from the row
    gr.Markdown("## Recommednations")
    output = ...
    
    # On Click submit button action
    submit_button.click(...)

if __name__ == "__main__":
    dashboard.launch()
