from __future__ import annotations
import re
import os
import uuid
import tempfile
from pathlib import Path
import cloudinary
import cloudinary.uploader
import httpx
from fastapi import HTTPException

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx","jpg", "jpeg", "png","svg"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

#cloudinary for fast loading of resumes

cloudinary.config(
    cloud_name="dbdws8xmv",
    api_key="632351763265899",
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "insert the key here"),
    secure=True
)


def ensure_upload_dir(base_dir: str = "uploads") -> str:
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    return base_dir


def save_upload(file_bytes: bytes, original_filename: str) -> str:
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError("File too large")
    
    ext = original_filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")

    # Create a temporary file and write the bytes to it
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_file:
        temp_file.write(file_bytes)
        temp_file_path = temp_file.name

    try:
        unique_name = f"resume_{uuid.uuid4().hex}"
        upload_result = cloudinary.uploader.upload(
            temp_file_path,
            resource_type="auto",
            public_id=unique_name,
            folder="resumes",
            overwrite=True
        )

        # Get secure URL and inject `fl_attachment` for forced download
        secure_url = upload_result["secure_url"]
        download_url = secure_url.replace("/upload/", "/upload/fl_attachment/")

        return download_url
    finally:
        # Ensure the temporary file is deleted
        os.unlink(temp_file_path)


#password validator

def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")
    return password

# put your secret in environment variable for safety
RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET")

async def verify_recaptcha(token: str) -> None:
    url = "https://www.google.com/recaptcha/api/siteverify"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data={"secret": RECAPTCHA_SECRET, "response": token})
    result = resp.json()

    if not result.get("success", False):
        raise HTTPException(status_code=400, detail="Invalid reCAPTCHA")

