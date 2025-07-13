from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_db, get_current_user
from app.models import File as FileModel
from app.utils import encrypt_id, decrypt_id
from fastapi.responses import FileResponse

router = APIRouter(prefix="/client", tags=["Client"])

@router.get("/files")
def list_files(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.user_type != "client":
        raise HTTPException(status_code=403, detail="Only client can access file list")
    files = db.query(FileModel).all()
    return [{"id": f.id, "filename": f.filename} for f in files]

@router.get("/download-file/{file_id}")
def generate_download_link(file_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.user_type != "client":
        raise HTTPException(status_code=403, detail="Only clients can download")
    enc_id = encrypt_id(file_id)
    return {"download_link": f"http://localhost:8000/client/download/{enc_id}", "message": "success"}

@router.get("/download/{enc_id}")
def download(enc_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.user_type != "client":
        raise HTTPException(status_code=403, detail="Only client can download")

    try:
        file_id = decrypt_id(enc_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid link")

    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file.filepath, filename=file.filename, media_type="application/octet-stream")
