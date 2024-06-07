import uuid

from fastapi import FastAPI, Query
from pgvector import Vector
from pydantic import BaseModel, Field

from app.chunking import chunk_text
from app.config import get_settings
from app.db import conn, init_db
from app.embeddings import local_embedding

app=FastAPI(title='RAGForge Platform', version='0.1.0')

