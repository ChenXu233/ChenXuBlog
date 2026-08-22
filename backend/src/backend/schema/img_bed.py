from pydantic import BaseModel, Field


class ImageUploadResponse(BaseModel):
    url: str = Field(..., description="Public URL of the uploaded image")
