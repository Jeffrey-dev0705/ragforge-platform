import hashlib
import math

DIM=64

def local_embedding(text: str) -> list[float]:
    v=[0.0]*DIM
    for token in text.lower().split():
        h=hashlib.sha256(token.encode()).digest(); i=int.from_bytes(h[:2],'big')%DIM
        v[i]+=1.0 if h[2]%2==0 else -1.0
    n=math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/n for x in v]
