from langchain_community.vectorstores.chroma import Chroma
# from langchain_community.s
from Utils import CustomEmbeddings, batch_splitter
from Utils import load_config
from typing import List
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
            persist_directory=self.config_vdb.get('path'),
            embedding_function=self.embedding_model
        )
    
    def __generate_chunk_ids(self, docs: List[str]):
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
            page = doc.metadata.get('page')
            current_page_id = f"{source}:{page}"

            if current_page_id == last_page_id:
                current_doc_idx += 1
            else:
                current_doc_idx = 0
            
            doc_idx = f"{current_page_id}:{current_doc_idx}"
            last_page_id = current_page_id

            doc.metadata['id'] = doc_idx
        

        return docs
    
    def add_data(self, docs):
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

    def __clear_database(self):
        if os.path.exists(self.config.get('path')):
            shutil.rmtree(self.config.get('path'))

    def __update_docs(self, docs: List[str]):
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
            print("✅ No documents to updated.")

