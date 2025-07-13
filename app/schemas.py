from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_type: str  # ops or client

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileUpload(BaseModel):
    filename: str

class DownloadResponse(BaseModel):
    download_link: str
    message: str
