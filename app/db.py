from contextlib import contextmanager

import psycopg
from pgvector.psycopg import register_vector

from app.config import get_settings


@contextmanager
def conn():
    c=psycopg.connect(get_settings().database_url); register_vector(c)
    try: yield c
    finally: c.close()

def init_db():
    with psycopg.connect(get_settings().database_url, autocommit=True) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS documents(
          id UUID PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT now())''')
        c.execute('''CREATE TABLE IF NOT EXISTS chunks(
          id UUID PRIMARY KEY, document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
          chunk_index INT NOT NULL, content TEXT NOT NULL, embedding vector(64) NOT NULL)''')
