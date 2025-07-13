from sqlalchemy.orm import Session
from app import models, utils
from app.schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    hashed_pw = utils.get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_pw, user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and utils.verify_password(password, user.password):
        return user
    return None
