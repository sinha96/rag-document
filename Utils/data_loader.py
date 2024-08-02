import bs4
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv('env')

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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    return splits


if __name__ == '__main__':
    print(pdf_loaders(path='../Documention_AWS')[:5])
