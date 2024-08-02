import os
from typing import List
from dotenv import load_dotenv
from Utils.config import load_config
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import Chroma


load_dotenv('env')
config = load_config(name=('model', 'embed'))

class CustomEmbeddings(Embeddings):
    """

    """
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return [self.model.encode().tolist() for d in documents]

    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0].tolist()


def embed(docs: list):
    """
    """
    embedding_model = CustomEmbeddings(model_name=config['name'])
    print(len(docs))
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory='./asset/'
    )

