import os

# Setting environment variable `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION` due to issues with importing 'langchain_chroma'
# Fix for protobuf compatibility issue with 'langchain_chroma' by enforcing Python implementation
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import pandas as pd
import gradio as gr

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from src.helper import recommend_books

# Loading environment variables from .env file
load_dotenv()

# Changing the working directory (as defined in the .env file, i.e, the parent directory) for data access
working_directory = os.getenv("WORKING_DIRECTORY")
os.chdir(working_directory)

# Loading in dataset with precomputed categories, emotion scores, and thumbnail URLs
books = pd.read_csv("data/books_emotions_and_thumbnail.csv")

# Preparing dropdown options for category and emotion filters
category_labels = ["All"] + sorted((books["base_categories"].unique()))
emotion_labels = ["All"] + sorted(["Anger", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Neutral"])

# Constructing each book description into a LangChain Document object
# (required for embedding and vector store)
document_object = [
    Document(
        page_content=row["description"],
        metadata={"source": str(row["isbn13"])}
    )
    for _, row in books.iterrows()
]

# Initialzing the embedding model from Google Generative AI
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001" )

# Creating a Chroma vector database from the book documents using the generated embeddings
db_books = Chroma.from_documents(document_object, embedding=embeddings)

# Intermediate function for `recommend_books` due to issues with Gardio
# Gradio-compatible wrapper function that injects global dataset and vector DB into the recommender
def recommend_books_inter(query: str, category: str, tone: str):
    # Assign global data variables
    books = globals()["books"]
    db_books = globals()["db_books"]
    return recommend_books(books, db_books, query, category, tone)

# Main UI block using Gradio
with gr.Blocks(theme=gr.themes.Glass()) as dashboard:
    gr.Markdown("# 📚 Book Recommender")

    # User inputs for filtering recommendations
    # Input row: user query, category filter, and emotion filter
    with gr.Row():
        query_filter = gr.Textbox(label="Enter book description", placeholder="A story about a rat set in France")
        category_filter = gr.Dropdown(choices=category_labels, label="Select a category", value="All")
        emotion_filter = gr.Dropdown(choices=emotion_labels, label="Select an emotional text", value="All")
        submit_button = gr.Button("Fetch Recommendations")
    
    # Output gallery for book recommendations
    gr.Markdown("## Recommendations")
    output = gr.Gallery(label="Recommended books based on your filters", columns=8, rows=3)
    
    # Binds the recommendation function to the submit button, and triggers on click
    submit_button.click(fn=recommend_books_inter,
                        inputs=[query_filter, category_filter, emotion_filter],
                        outputs=output)

# Launches the Gradio app
if __name__ == "__main__":
    dashboard.launch()
