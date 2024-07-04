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

@app.get('/api/v1/search')
def search(q:str=Query(min_length=2),limit:int=Query(5,ge=1,le=20)):
    v=Vector(local_embedding(q))
    with conn() as c:
        rows=c.execute('''SELECT c.document_id::text,d.title,c.chunk_index,c.content,c.embedding <=> %s AS distance
          FROM chunks c JOIN documents d ON d.id=c.document_id ORDER BY c.embedding <=> %s LIMIT %s''',(v,v,limit)).fetchall()
    return [{'document_id':r[0],'title':r[1],'chunk_index':r[2],'content':r[3],'distance':float(r[4])} for r in rows]

