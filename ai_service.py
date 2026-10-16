import httpx
from sqlalchemy.orm import Session
from crud import get_student_stats


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


async def query_ollama(db: Session, question: str) -> str:
    stats = get_student_stats(db)

    context = f"""
Student Database Statistics:
- Total Students: {stats['total_students']}
- Students by Course: {stats['by_course']}
"""

    prompt = f"""You are a helpful assistant that answers questions about a student database.
Use ONLY the provided context to answer. Do not make up information.
If the question cannot be answered from the context, say so.

Context:
{context}

Question: {question}

Answer:"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No response from model")
    except httpx.ConnectError:
        return "Error: Cannot connect to Ollama. Make sure Ollama is running at http://localhost:11434"
    except httpx.TimeoutException:
        return "Error: Request to Ollama timed out"
    except Exception as e:
        return f"Error: {str(e)}"