from Utils.data_loader import pdf_loaders
from Embedder import embed
from datetime import datetime as time

if __name__ == '__main__':
    st = time.now()
    print('>>> Loading documents.')
    st_proc = time.now()
    doc_split = pdf_loaders(path='../Documention_AWS')
    print(f'>>> Loaded document in {time.now() - st_proc}s')
    print('>>> Staring vectoriser')
    st_proc = time.now()
    embed(docs=doc_split)
    print(f'>>> Embedding done in {time.now() - st_proc}s')
    print(f'>>> Completed process in {time.now() - st}s')
