import os
import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS ayarlarını daha spesifik ve güvenilir yap
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Frontend port
        "http://127.0.0.1:8080",
        "http://10.252.18.16:8080",  # IP üzerinden erişim için
        "*"  # Geliştirme için tüm originlere izin
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class TodoCreate(BaseModel):
    text: str

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'todoapp'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
    )

@app.get("/")
def read_root():
    return {"message": "todo backend çalışıyor!"}

@app.get("/todos")
def get_todos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, created_at FROM todos ORDER BY created_at DESC")
    todos = []
    for row in cursor.fetchall():
        todos.append({
            "id": row[0],
            "text": row[1],
            "created_at": str(row[2])
        })
    cursor.close()
    conn.close()
    return todos

@app.post("/todos")
def create_todo(todo: TodoCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (text) VALUES (%s) RETURNING id, created_at", 
        (todo.text,)
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "id": row[0],
        "text": todo.text,
        "created_at": str(row[1])
    }

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return {"error": "Todo bulunamadı"}
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Todo silindi"}

# Explicit OPTIONS handler (gerekirse)
@app.options("/{full_path:path}")
def handle_options(full_path: str):
    return {"message": "OK"}