from fastapi import FastAPI, File, UploadFile
from DataBase import VectorData
from Utils import pdf_loaders
from typing import List
import tempfile
import warnings
import os

warnings.filterwarnings('ignore')

app = FastAPI()
vdb = VectorData()

@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    global vdb
    with tempfile.TemporaryDirectory() as tmpdirname:
        for file in files:
            file_path = os.path.join(tmpdirname, file.filename)
            with open(file_path, "wb") as f:
                contents = await file.read()
                f.write(contents)
        doc_split = pdf_loaders(tmpdirname)
        vdb.add_data(docs=doc_split)
        
    return {"files_processed": len(files)}

    return {"message": "Hello World"}


@app.get("/results/")
async def fetch_answer(question: str, top_doc: int):
    global vdb
    results = vdb.query_data(q=question, top_k=top_doc)
    contexts = [doc[0].page_content for doc in results]
    context = '\n ---------- \n'.join(contexts)
    sources = [doc[0].metadata.get('source', '') for doc in results]
    pages = [doc[0].metadata.get('page', '') for doc in results]
    similarity_score = [doc[1] for doc in results]

    return {"context": context, "source": sources, 'results': results, 'pages': pages, 'similarity_score': similarity_score, "User_query": question}

