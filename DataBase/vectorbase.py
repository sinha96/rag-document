from langchain_community.vectorstores.chroma import Chroma
from Utils import CustomEmbeddings, batch_splitter, load_config, sha_generator
from langchain_core.documents import Document
from typing import List, Tuple
import shutil
import os

class VectorData:
    def __init__(self):
        self.config_vdb = load_config(name=('database',))
        self.config_model = load_config(name=('model', 'embed'))
        # Initiating embedding model
        self.embedding_model = CustomEmbeddings(
            model_name=self.config_model.get('name')
        )

        # Loading Vector DB
        self.db = Chroma(
            collection_name='rag-docs',
            persist_directory=self.config_vdb.get('path'),
            embedding_function=self.embedding_model
        )
    
    def __generate_chunk_ids(self, docs: List[Document]):
        """
        Generates id for all the chucks to keep tracking duplicate records

        :param docs: List of document chunks

        :rtype: List
        :return: Chunks with id

        """

        last_page_id = None
        current_doc_idx = 0

        for doc in docs:
            source = doc.metadata.get('source')
            source = source.split('/')[-1]
            page = doc.metadata.get('page')
            current_page_id = f"{source}:{page}"

            if current_page_id == last_page_id:
                current_doc_idx += 1
            else:
                current_doc_idx = 0
            
            doc_idx = sha_generator(f"{current_page_id}:{current_doc_idx}")
            last_page_id = current_page_id

            doc.metadata['id'] = doc_idx
        

        return docs
    
    def add_data(self, docs: List[Document]):
        """
        """
        # Generate ids for chucks
        docs = self.__generate_chunk_ids(docs=docs)

        # Add or Update the documents.
        # Get existing ids in the database
        existing_items = self.db.get(include=[]) 
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        new_docs = []
        existing_docs = []
        for doc in docs:
            if doc.metadata["id"] not in existing_ids:
                new_docs.append(doc)
            else:
                existing_docs.append(doc)

        if len(new_docs):
            print(f"👉 Adding new documents: {len(new_docs)}")
            for batch in batch_splitter(documents=new_docs, batch_size=self.config_model.get('max_length')):
                new_chunk_ids = [doc.metadata["id"] for doc in batch]
                self.db.add_documents(batch, ids=new_chunk_ids)
                self.db.persist()
        else:
            print("✅ No new documents to add")
            self.__update_docs(docs=existing_docs)

    def _clear_database(self):
        existing_items = self.db.get(include=[]) 
        existing_ids = set(existing_items["ids"])
        self.db.delete(ids=existing_ids)

    def __update_docs(self, docs: List[Document]):
        """
        """
        
        update_doc = []
        for doc in docs:
            idx = doc.metadata.get('id')
            exist_doc = self.db.get(ids=[idx])

            incoming_doc = doc.page_content
            exist_doc = exist_doc['documents'][0]
            if incoming_doc != exist_doc: 
                update_doc.append(doc)
        if update_doc:
            print(f"👉 Updating existing documents: {len(update_doc)}")
            for batch in batch_splitter(documents=update_doc, batch_size=self.config_model.get('max_length')):
                update_chunk_ids = [doc.metadata["id"] for doc in batch]
                self.db.update_documents(documents=batch, ids=update_chunk_ids)
        else:
            print("✅ No documents to update.")

    def query_data(self, q, top_k: int) -> List[Tuple[Document, float]]:
        """
        query data from DataBase

        """
        results = self.db.similarity_search_with_score(
            query=q,
            k=top_k
        )

        return results
