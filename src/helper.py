import os

# Setting environment variable `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION` due to issues with importing 'langchain_chroma'
# Fix for protobuf compatibility issue with 'langchain_chroma' by enforcing Python implementation
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import pandas as pd
from langchain_chroma import Chroma

# ---------------------------------------------
# Function: retrieve_semantic_recommendations
# ---------------------------------------------
# Description:
# Performs a semantic similarity search using the Chroma vector database
# and retrieves the most relevant books from the original dataset.
#
# Parameters:
# - books (pd.DataFrame): The original dataset of books
# - db_books (Chroma): Chroma vector store of book descriptions
# - query (str): User input text to search semantically
# - no_of_recc (int): Number of top recommendations to retrieve
#
# Returns:
# - pd.DataFrame: A filtered DataFrame containing top matching books
def retrieve_semantic_recommendations(books: pd.DataFrame, db_books: Chroma, query: str, no_of_recc: int) -> pd.DataFrame:
    response_books = db_books.similarity_search(query, k=no_of_recc)
    isbn_list = [int(doc_object.metadata["source"]) for doc_object in response_books]
    return books[books["isbn13"].isin(isbn_list)].head(no_of_recc)

# ---------------------------------------------
# Function: filter_books
# ---------------------------------------------
# Description:
# Applies category and emotional tone filters to a given set of books.
#
# Parameters:
# - books (pd.DataFrame): DataFrame of semantically similar books
# - category (str): Selected category to filter (e.g., "Fiction")
# - tone (str): Selected emotion to prioritize (e.g., "Joy")
# - final_no_of_recc (int): Final number of books to return after filtering
#
# Returns:
# - pd.DataFrame: Filtered and optionally sorted book recommendations
def filter_books(books: pd.DataFrame, category: str, tone: str, final_no_of_recc: int) -> pd.DataFrame:
    if category != "All":
        books = books[books["base_categories"] == category]

     # Truncate to final count before applying tone filter
    books = books.head(final_no_of_recc)

    if tone != "All":
            books.sort_values(by=tone.lower(), ascending=False, inplace=True)

    return books

# ---------------------------------------------
# Function: recommend_books
# ---------------------------------------------
# Description:
# Pipeline function to generate book recommendations:
# 1. Retrieves top matches based on semantic similarity
# 2. Applies category and tone filters
# 3. Formats results for UI rendering
#
# Parameters:
# - books (pd.DataFrame): Book dataset
# - db_books (Chroma): Chroma vector store
# - query (str): User input description
# - category (str): Category filter
# - tone (str): Emotion filter
# - inital_no_of_recc (int): Initial number of semantic matches to consider
# - final_no_of_recc (int): Final number of filtered results to return
#
# Returns:
# - List[Tuple[str, str]]: List of (thumbnail URL, caption) pairs for display
def recommend_books(books: pd.DataFrame, db_books: Chroma, query: str, category: str, tone: str,
                    inital_no_of_recc: int = 50, final_no_of_recc: int = 24):
    
    # Step 1: Semantic search
    recommendations = retrieve_semantic_recommendations(books, db_books, query, inital_no_of_recc)

    # Step 2: Filter based on user-selected category and tone
    filtered_recommendations = filter_books(recommendations, category, tone, final_no_of_recc)

    # Record: Print filtered results to terminal
    print(filtered_recommendations)

    # Step 3: Prepare formatted results for UI (Gradio gallery expects image-caption pairs)
    # Create a list of (thumbnail, caption) pairs for display
    results = []
    for _, row in filtered_recommendations.iterrows():
        caption = f"{row['title']} by {row['authors']}: {row['description']}"
        results.append((row["large_thumbnail"], caption))
        
    return results
