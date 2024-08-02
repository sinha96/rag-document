import bs4
import toml
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document
load_dotenv('env')


def split_cleanser(docs: List[Document]):
    """
    """
    for doc in docs:
        doc.page_content = doc.page_content.lower()
    return docs

def web_loader(urls: list) -> object:
    """
    """
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
                )
            ),
    )
    docs = loader.load()

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits


def pdf_loaders(path: str) -> object:
    """
    """
    loader = PyPDFDirectoryLoader(
        path=path
    )
    docs = loader.load()
    
    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    splits = split_cleanser(docs=splits)
    return splits


def load_config(name: List[str]):
    with open('pyproject.toml', 'r') as f:
        config = toml.load(f)
    if len(name) > 1:
        return config[name[0]][name[1]]
    else:
        return config[name[0]]
    

def batch_splitter(documents: List[str], batch_size: int):
    """
    Splits chucks in batches for ingestion by vector DB

    :param doucments: List of text chucks from documents
    :param batch_size: Size batch

    :rtype: List
    :return: batches of chunks

    """
    for idx in range(0, len(documents), batch_size):
        yield documents[idx:idx + batch_size]


class CustomEmbeddings(Embeddings):
    """
    Custom Embedder
    
    """
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return [self.model.encode(d).tolist() for d in documents]

    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0].tolist()

if __name__ == '__main__':
    import os
    print(os.path.isdir('../dummy/'))
    print(pdf_loaders(path='../dummy/'))
