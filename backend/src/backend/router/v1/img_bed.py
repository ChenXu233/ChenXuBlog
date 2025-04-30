import hashlib
import io

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image

from backend.config import CONFIG

img_bed = APIRouter(prefix="/apis/v1/img_bed", tags=["img_bed"])


@img_bed.post("/")
async def upload_image(request: Request, image: UploadFile = File(...)):
    image_content = await image.read()

    image_hash = hashlib.sha256(image_content).hexdigest()

    img = Image.open(io.BytesIO(image_content))
    if not img.format:
        raise HTTPException(status_code=400, detail="Invalid image format")
    image_format = img.format.lower()

    image_filename = f"{image_hash}.{image_format}"
    image_path = CONFIG.IMAGE_BED_PATH / image_filename

    if image_path.exists():
        raise HTTPException(status_code=409, detail="Image already exists")

    with open(image_path, "wb") as f:
        f.write(image_content)

    image_url = request.url_for("upload_image", image_hash=image_filename)

    return JSONResponse(content={"url": image_url})


@img_bed.get("/{image_hash}")
async def get_image(image_hash: str):
    matching_files = list(CONFIG.IMAGE_BED_PATH.glob(f"{image_hash}*"))
    if not matching_files:
        raise HTTPException(status_code=404, detail="Image not found")

    image_path = matching_files[0]

    return FileResponse(image_path)
