###
# Création d'un RAG à partir des docs Outscale et de la base de données Chroma
###
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pathlib import Path
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma

import shutil

from extract_analyze_docs import process_sections_docs

def longchain_create_documents():
    all_sections = process_sections_docs()
    text_docs = [
        Document(page_content=section.pop("content"), metadata=section)
        for section in all_sections
    ]
    print(f"Extracted {len(text_docs)} text documents")
    return text_docs

def initialize_embeddings_vector(text_docs):
    print("Initializing Chroma vector store...")
    # Initialize the Chroma vector store
    # !! D:\wutemp\p8\workspace\rag\rag.py:157: LangChainDeprecationWarning: The class `HuggingFaceEmbeddings` was deprecated in LangChain 0.2.2 and will be removed in 1.0. An updated version of the class exists in the :class:`~langchain-huggingface package and should be used
    # instead. To use it run `pip install -U :class:`~langchain-huggingface` and import as `from :class:`~langchain_huggingface import HuggingFaceEmbeddings``.
    # https://python.langchain.com/docs/integrations/text_embedding/sentence_transformers/
    embeddings = SentenceTransformerEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    print(f"Embedding model loaded: {embeddings.model_name}")
    print(f"Embedding : {embeddings}")
    return embeddings


def chroma_create_db():
    text_docs = longchain_create_documents()
    embeddings = initialize_embeddings_vector(text_docs)
    persist_directory = "./chroma"
    print(f"persisting to {persist_directory}")

    dirpath = Path(persist_directory)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    db = Chroma.from_documents(
        text_docs,
        embeddings,
        collection_name="outscale",
        persist_directory=persist_directory,
    )
    db.persist()
