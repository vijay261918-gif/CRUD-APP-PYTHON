# Student CRUD API

A FastAPI REST API for managing student records with SQLite database and optional AI queries via Ollama.

## Prerequisites

- Python 3.10 or higher
- Git
- (Optional) [Ollama](https://ollama.com) for the AI query endpoint

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone <your-repo-url>
cd student_crud_project

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1     # Windows (PowerShell)
source venv/bin/activate        # Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
python -m uvicorn main:app --reload
```

API runs at: **http://localhost:8000**  
Swagger UI: **http://localhost:8000/docs**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Create student |
| GET | `/students` | List students (optional `?course=` filter) |
| GET | `/students/{id}` | Get student by ID |
| PUT/PATCH | `/students/{id}` | Update student |
| DELETE | `/students/{id}` | Delete student |
| POST | `/ai/query` | Ask AI about student data (requires Ollama) |

## Example Requests

```bash
# Create
curl -X POST http://localhost:8000/students -H "Content-Type: application/json" -d '{"name":"John","date_of_birth":"2000-01-15","email":"john@example.com","course":"CS"}'

# List all
curl http://localhost:8000/students

# Filter by course
curl "http://localhost:8000/students?course=CS"

# Get one
curl http://localhost:8000/students/1

# Update
curl -X PATCH http://localhost:8000/students/1 -H "Content-Type: application/json" -d '{"course":"Data Science"}'

# Delete
curl -X DELETE http://localhost:8000/students/1

# AI query (needs Ollama running)
curl -X POST http://localhost:8000/ai/query -H "Content-Type: application/json" -d '{"query":"How many students?"}'
```

## Project Structure

```
├── main.py          # FastAPI app & routes
├── models.py        # SQLAlchemy Student model
├── schemas.py       # Pydantic validation schemas
├── crud.py          # Database operations
├── database.py      # SQLite connection
├── ai_service.py    # Ollama integration
└── requirements.txt # Dependencies
```

## Optional: AI Queries

Install Ollama and run:
```bash
ollama pull llama3.2:1b
ollama serve
```
Then POST to `/ai/query` with a question about the data.