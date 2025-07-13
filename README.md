# 🔐 Secure File Sharing System (FastAPI)

A back-end project that implements a secure, role-based file-sharing system between two user types: **Ops** and **Client**. Built with modern Python tools like FastAPI, PostgreSQL, JWT, and encrypted download URLs.

---

## 📦 Features

### 👤 Ops User
- ✅ Login
- ✅ Upload files (`.pptx`, `.docx`, `.xlsx` only)

### 👥 Client User
- ✅ Sign up
- ✅ Receive email verification link
- ✅ Login (only after verification)
- ✅ View list of uploaded files
- ✅ Generate encrypted download links
- ✅ Download files securely

### 🔐 Security & Best Practices
- Passwords hashed with `bcrypt`
- JWT-based token authentication
- Email verification for client users
- Download links encrypted via `Fernet`
- File type validation on upload
- Role-based access control enforced

---

## 🧰 Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (via SQLAlchemy ORM)
- **Auth:** OAuth2 + JWT (`jose`)
- **Security:** `passlib`, `cryptography.fernet`
- **Email:** SMTP (via Mailtrap.io or Gmail SMTP)
- **Testing:** Pytest + FastAPI TestClient
- **Deployment:** Docker-ready

---

## 🚀 Project Structure

file_share_system/
├── app/
│ ├── routers/ # Route logic: auth, ops, client
│ ├── models.py # Database models
│ ├── schemas.py # Pydantic request/response validation
│ ├── utils.py # Hashing, JWT, encryption tools
│ ├── crud.py # Database interactions
│ ├── auth.py # Auth functions and dependencies
│ ├── database.py # Database setup
│ └── main.py # Main FastAPI app
├── tests/ # Full test suite
├── uploads/ # Uploaded files
├── .env # Environment config
├── Dockerfile # Optional container support
├── README.md # You're here!


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```git clone https://github.com/yourusername/file_share_system.git
cd file_share_system
```
### 2. Install Dependencies

- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

### 3. Configure .env

- DATABASE_URL=postgresql://postgres:yourpassword@localhost/fileshare
- SECRET_KEY=<your_generated_secret>
- ALGORITHM=HS256
- EMAIL_USER=your@mailtrap.email
- EMAIL_PASSWORD=your_mailtrap_password
- EMAIL_HOST=smtp.mailtrap.io
- EMAIL_PORT=587

### 4. Run the App

- uvicorn app.main:app --reload

## 🔍 API Endpoints
# 🧑‍💼 Auth
- POST /auth/signup
- GET /auth/verify/{token}
- POST /auth/login

# 🧑‍🏭 Ops User
- POST /ops/upload

# 👤 Client User
- GET /client/files
- GET /client/download-file/{file_id}
- GET /client/download/{encrypted_id}

## 📦 Deployment (Optional Docker)

- docker build -t secure-fileshare .
- docker run -p 8000:8000 secure-fileshare

## 🙌 Author
- Built by Tushansh Bajaj.
- Contact me at [tbb@gmail.com] for questions or improvements!
