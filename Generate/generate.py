from typing import Dict
import requests
import json


class GenerateResponse:
    def __init__(self):
        self.results = None
        self.__model_url = "http://localhost:11434/api/generate"
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.payload = {
            "model": "llama3.1",
            "stream": False,
        }
    
    def generate_response(self, similar_doc: Dict, user_query: str) -> Dict:
        """
        """
        contexts = [doc[0].page_content for doc in similar_doc]
        context = '\n ---------- \n'.join(contexts)
        sources = [doc[0].metadata.get('source', '') for doc in similar_doc]
        pages = [doc[0].metadata.get('page', '') for doc in similar_doc]
        similarity_score = [doc[1] for doc in similar_doc]

        template = """
        ### System:
        You are an respectful and honest assistant. You have to answer the user's \
        questions using only the context provided to you. If you don't know the answer, \
        just say you don't know. Don't try to make up an answer.

        ### Context:
        {context}

        ### User:
        {question}

        ### Response:
        """

        self.payload['prompt'] = template.format(context=context, question=user_query)
        response = requests.post(
            self.__model_url, 
            data=json.dumps(self.payload), 
            headers=self.headers
        )
        response = response.json()
        response['source'] = sources
        response['pages'] = pages
        response['similarity_score'] = similarity_score
        response['context'] = self.payload.get('prompt')
        # response['user_query'] = user_query
        return response



