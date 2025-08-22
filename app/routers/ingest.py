# upload and parsing pdf's
# app/routers/ingest.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
import os
import tempfile

from app.services.pdf_parser import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.embedder import get_embedding
from app.db.tidb import execute_query

router = APIRouter()

@router.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...), topic: str = "General", user_id: str = "demo-user"):
    # Save temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    # Step 1: Extract Text
    text = extract_text_from_pdf(tmp_path)

    # Step 2: Chunk Text
    chunks = chunk_text(text)

    # Step 3–5: Embed & store in DB
    for chunk in chunks:
        embedding = get_embedding(chunk)
        chunk_id = str(uuid4())
        query = """
        INSERT INTO chunks (id, user_id, topic, source, embedding, chunk_text)
        VALUES (%s, %s, %s, %s, VECTOR[%s], %s)
        """
        try:
            execute_query(query, (
                chunk_id,
                user_id,
                topic,
                file.filename,
                ",".join(map(str, embedding)),  # Convert list → string
                chunk
            ))
        except Exception as e:
            print(f"Failed to insert chunk: {e}")

    os.remove(tmp_path)
    return {"status": "success", "chunks_stored": len(chunks)}
