from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from app.auth import get_db, get_current_user
from app.models import File as FileModel

router = APIRouter(prefix="/ops", tags=["Ops"])

ALLOWED_EXT = ["pptx", "docx", "xlsx"]
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_file(upload: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.user_type != "ops":
        raise HTTPException(status_code=403, detail="Only Ops user can upload")
    
    ext = upload.filename.split(".")[-1]
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = f"{UPLOAD_DIR}/{upload.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    db_file = FileModel(filename=upload.filename, filepath=file_path, uploader_id=current_user.id)
    db.add(db_file)
    db.commit()
    return {"message": "File uploaded successfully"}
