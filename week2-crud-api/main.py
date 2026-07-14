from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ---------- Root & Health (Stage 1) ----------

@app.get("/", summary="API info", description="Returns basic info about this API")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health", summary="Health check", description="Confirms the server is running")
def health_check():
    return {"status": "ok"}

# ---------- In-memory data (Stage 2) ----------

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish assignment", "done": False},
    {"id": 3, "title": "Read a book", "done": True},
]

next_id = 4  # tracks the next free id

# ---------- Read endpoints (Stage 2) ----------

@app.get("/tasks", summary="List all tasks", description="Returns every task currently stored")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="Get one task", description="Returns a single task by id, or 404 if not found")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# ---------- Create endpoint (Stage 3) ----------

class TaskCreate(BaseModel):
    title: Optional[str] = None

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_id
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task

# ---------- Update & Delete endpoints (Stage 4) ----------

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                if not update.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
