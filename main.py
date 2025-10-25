from fastapi import FastAPI, File, HTTPException, Query, UploadFile
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

origins = [
    "http://localhost:3000",
    "https://graphize.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class Image(BaseModel):
    id: Optional[str] = None
    image_url: str
    user_id: str

@app.options("/images")
async def options_images():
    return JSONResponse(content={"message": "CORS is ready to go!"})

@app.options("/images/{image_id}")
async def options_image_id(image_id: str):
    return JSONResponse(content={"message": "CORS is ready to go!"})

@app.get("/")
async def root():
    return {"message": "Successfully Created!"}

@app.get("/images", response_model=List[Image])
async def get_saves(user_id: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"id": row["id"], "image_url": row["image_url"], "user_id": row["user_id"]} for row in rows]

@app.post("/images", response_model=Image)
async def create_save(data: Image):
    conn = get_db()
    cur = conn.cursor()
    image_id = uuid.uuid4().hex
    cur.execute('INSERT INTO images (id, image_url, user_id) VALUES (?, ?, ?)', (image_id, data.image_url, data.user_id))
    conn.commit()
    conn.close()
    return { "id": image_id, "image_url": data.image_url }

@app.delete("/images/{image_id}")
async def delete_save(image_id: str, user_id: Optional[str] = Query(None)):
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE id = ? AND user_id = ?", (image_id, user_id))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=403, detail="Forbidden")
    cur.execute("DELETE FROM images WHERE id = ?", (image_id,))
    conn.commit()
    conn.close()
    return {"message": "Deleted"}
