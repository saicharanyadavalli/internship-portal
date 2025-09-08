from __future__ import annotations
import re
import os
import uuid
from pathlib import Path
import cloudinary
import cloudinary.uploader

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
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


def save_upload(file_bytes: bytes, original_filename: str, base_dir: str = "uploads") -> str:
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError("File too large")
    ext = original_filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")
    unique_name = f"resume_{uuid.uuid4().hex}"
    upload_result = cloudinary.uploader.upload(
        file_bytes,
        resource_type="auto",
        public_id=unique_name,
        folder="resumes",
        overwrite=True
    )
    return upload_result["secure_url"]

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
