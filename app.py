import pandas as pd
import numpy as np

import gradio as gr

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma

# Loading environment variables from .env file
load_dotenv()

