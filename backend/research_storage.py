from __future__ import annotations
from langchain_community.retrievers import WikipediaRetriever
import operator
import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import TypedDict, List, Optional, Literal, Annotated
from pydantic import BaseModel, Field
from typing import List

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langgraph.types import Send

from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
import arxiv
import requests
 

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_huggingface import HuggingFaceEmbeddings
import requests
import base64

import time




emb=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_Store="Vectore_store"

if not os.path.exists(vector_Store):
    os.makedirs(vector_Store)
    
    


def get_text(ans):
    return "\n\n".join(text for text in ans)


def add_to_vector_store(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents([
        Document(page_content=text)
    ])

    index_file = os.path.join(vector_Store, "index.faiss")

    # Existing DB
    if os.path.exists(index_file):
        vector_store = FAISS.load_local(
            vector_Store,
            emb,
            allow_dangerous_deserialization=True
        )

        vector_store.add_documents(docs)

    # First time create DB
    else:
        vector_store = FAISS.from_documents(
            docs,
            emb
        )

    vector_store.save_local(vector_Store)


