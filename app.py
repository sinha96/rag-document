from fastapi import FastAPI, File, UploadFile
from Generate import GenerateResponse
from DataBase import ingest_document
from Retrieve import retriever
from typing import List
import tempfile
import warnings
import os

warnings.filterwarnings('ignore')

app = FastAPI()

@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    global vdb
    with tempfile.TemporaryDirectory() as tmpdirname:
        for file in files:
            file_path = os.path.join(tmpdirname, file.filename)
            with open(file_path, "wb") as f:
                contents = await file.read()
                f.write(contents)
        ingest_document(tmpdirname)
        
    return {"files_processed": len(files)}

    return {"message": "Hello World"}


@app.get("/results/")
async def fetch_answer(question: str, top_doc: int):
    similar_docs = retriever(question=question, top_doc=top_doc)
    response_generator = GenerateResponse()
    response = response_generator.generate_response(
        similar_doc=similar_docs,
        user_query=question
    )
    return response
    

    

