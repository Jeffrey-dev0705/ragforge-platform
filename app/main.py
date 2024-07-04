import uuid

from fastapi import FastAPI, Query
from pgvector import Vector
from pydantic import BaseModel, Field

from app.chunking import chunk_text
from app.config import get_settings
from app.db import conn, init_db
from app.embeddings import local_embedding

app=FastAPI(title='RAGForge Platform', version='0.1.0')

class DocumentIn(BaseModel):
    title:str=Field(min_length=1,max_length=300)
    content:str=Field(min_length=20)

@app.on_event('startup')
def startup(): init_db()

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/api/v1/documents')
def ingest(x:DocumentIn):
    did=uuid.uuid4(); s=get_settings(); parts=chunk_text(x.content,s.chunk_size,s.chunk_overlap)
    with conn() as c, c.transaction():
        c.execute('INSERT INTO documents(id,title,content) VALUES(%s,%s,%s)',(did,x.title,x.content))
        for i,part in enumerate(parts):
            c.execute('INSERT INTO chunks(id,document_id,chunk_index,content,embedding) VALUES(%s,%s,%s,%s,%s)',
                      (uuid.uuid4(),did,i,part,Vector(local_embedding(part))))
    return {'id':str(did),'chunks':len(parts)}

