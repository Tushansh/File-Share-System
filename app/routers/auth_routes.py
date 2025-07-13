from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, schemas, models, utils
from app.auth import get_db
from app.utils import create_access_token
import smtplib
from email.mime.text import MIMEText
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db, user)
    
    # Send verification email
    token = utils.encrypt_id(new_user.id)
    link = f"http://localhost:8000/auth/verify/{token}"
    
    send_verification_email(user.email, link)
    return {"message": "Verification email sent", "verify_url": link}

@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        user_id = utils.decrypt_id(token)
    except:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

def send_verification_email(to_email: str, link: str):
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    host = os.getenv("EMAIL_HOST")
    port = int(os.getenv("EMAIL_PORT"))

    msg = MIMEText(f"Click the link to verify your email: {link}")
    msg["Subject"] = "Verify your email"
    msg["From"] = user
    msg["To"] = to_email

    with smtplib.SMTP(host, port) as server:
        server.login(user, password)
        server.send_message(msg)
