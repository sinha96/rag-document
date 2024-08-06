from DataBase import VectorData
from typing import List


vdb = VectorData()

def retriever(question: str, top_doc: int = 1) -> List:
    """
    """
    global vdb
    results = vdb.query_data(q=question, top_k=top_doc)
    return results