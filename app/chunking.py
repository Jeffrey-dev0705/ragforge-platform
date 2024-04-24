def chunk_text(text: str, size: int=700, overlap: int=100) -> list[str]:
    text=' '.join(text.split())
        if end < len(text):
            b=part.rfind(' ')
            if b > size//2: end=start+b; part=text[start:end]
        out.append(part.strip())
        if end>=len(text): break
        start=max(start+1,end-overlap)
    return out
