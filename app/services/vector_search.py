from app.db.tidb import get_connection
import numpy as np

def search_similar_chunks(embedding: list[float], top_k: int = 5) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    placeholder = ",".join(["%s"] * len(embedding))
    query = f"""
        SELECT id, chunk_text, topic, source, L2_DISTANCE(embedding, VECTOR[{placeholder}]) AS distance
        FROM chunks
        ORDER BY distance ASC
        LIMIT {top_k}
    """
    cursor.execute(query, tuple(embedding))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
