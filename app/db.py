from contextlib import contextmanager

import psycopg
from pgvector.psycopg import register_vector

from app.config import get_settings


@contextmanager
def conn():
    c=psycopg.connect(get_settings().database_url); register_vector(c)
    try: yield c
    finally: c.close()

