from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uuid
import tempfile
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import sqlite3
from db import get_db, init_db

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için tüm kaynaklara izin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Image(BaseModel):
    id: Optional[str] = None
    image_url: str

@app.get("/")
async def root():
    return {"message": "Successfully Created!"}

@app.get("/images", response_model=List[Image])
async def get_saves():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM images")
    rows = cur.fetchall()
    return [{"id": row["id"], "image_url": row["image_url"]} for row in rows]

@app.post("/images", response_model=Image)
async def create_save(image: Image):
    conn = get_db()
    cur = conn.cursor()
    image_id = uuid.uuid4().hex
    cur.execute('INSERT INTO images (id, image_url) VALUES (?, ?)', (image_id, image.image_url))
    conn.commit()
    return { "id": image_id, "image_url": image.image_url }

@app.delete("/images/{image_id}")
async def delete_save(image_id: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM images WHERE id = ?", (image_id,))
    conn.commit()
    return {"Message": "Deleted"}
