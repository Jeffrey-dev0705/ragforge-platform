from app.chunking import chunk_text
from app.embeddings import DIM, local_embedding


def test_chunking():
    assert len(chunk_text('word '*500,200,30))>1

