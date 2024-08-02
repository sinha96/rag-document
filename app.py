from Utils import pdf_loaders
from DataBase import VectorData
from datetime import datetime as time
import warnings
import argparse

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    st = time.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    vdb = VectorData()
    if args.reset:
        print("✨ Clearing Database")
        vdb.__clear_database()
    print('>>> Loading documents.')
    st_proc = time.now()
    doc_split = pdf_loaders(path='../../Documention_AWS')
    print(f'>>> Loaded document in {time.now() - st_proc}s')
    print('>>> Staring vectoriser')
    st_proc = time.now()
    vdb.add_data(docs=doc_split)
    print(f'>>> Embedding done in {time.now() - st_proc}s')
    print(f'>>> Completed process in {time.now() - st}s')
