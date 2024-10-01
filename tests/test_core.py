from app.chunking import chunk_text
from app.embeddings import DIM, local_embedding


def test_chunking():
    assert len(chunk_text('word '*500,200,30))>1

def test_embedding():
    a=local_embedding('hello world'); b=local_embedding('hello world')
    assert a==b and len(a)==DIM
