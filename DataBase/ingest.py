from DataBase import VectorData
from Utils import pdf_loaders
from typing import List

vdb = VectorData()

def ingest_document(path: str) -> None:
    """
    """
    doc_split = pdf_loaders(path=path)
    vdb.add_data(docs=doc_split)