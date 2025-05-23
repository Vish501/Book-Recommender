import os

# Setting environment variable `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION` due to issues with importing 'langchain_chroma'
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import pandas as pd
from langchain_chroma import Chroma

# Function to retrieve all the recommendations as a dataframe
# Inputs - Dataset, Chroma vector database, query, number of recommandations
# Outputs - List of Books as a df
def retrieve_semantic_recommendations(books: pd.DataFrame, db_books: Chroma, query: str, no_of_recc: int) -> pd.DataFrame:
    response_books = db_books.similarity_search(query, k=no_of_recc)
    isbn_list = [int(doc_object.metadata["source"]) for doc_object in response_books]
    return books[books["isbn13"].isin(isbn_list)].head(no_of_recc)

# Function to filter books based on category and tone
def filter_books(books: pd.DataFrame, category: str, tone: str, final_no_of_recc: int) -> pd.DataFrame:
    if category != "All":
        books = books[books["base_categories"] == category]

    books = books.head(final_no_of_recc)
    if tone != "All":
            books.sort_values(by=tone.lower(), ascending=False, inplace=True)

    return books

# Function to recommend books based on semantic similarity and optional filters
# Inputs - Dataset, Chroma vector database, query, category, tone, name, initial top_k, final top_k
# Outputs - List of (thumbnail, caption) tuples to display in the UI
def recommend_books(books: pd.DataFrame, db_books: Chroma, query: str, category: str, tone: str,
                    inital_no_of_recc: int = 50, final_no_of_recc: int = 24):

    recommendations = retrieve_semantic_recommendations(books, db_books, query, inital_no_of_recc)
    filtered_recommendations = filter_books(recommendations, category, tone, final_no_of_recc)
    print(filtered_recommendations) ### Terminal Output

    # Create a list of (thumbnail, caption) pairs for display
    results = []
    for _, row in filtered_recommendations.iterrows():
        caption = f"{row['title']} by {row['authors']}: {row['description']}"
        results.append((row["large_thumbnail"], caption))
    return results
