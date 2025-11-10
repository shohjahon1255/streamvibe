import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".jfif", ".tiff")

def save_file(image: UploadFile):
    ext = os.path.splitext(image.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File format not supported.")

    os.makedirs("images", exist_ok=True)

    safe_filename = f"{uuid.uuid4()}{ext}"
    file_location = os.path.join("images", safe_filename)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(image.file, f)

    return file_location