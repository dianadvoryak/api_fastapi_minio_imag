from fastapi import UploadFile
from pydantic import BaseModel

class Image(BaseModel):
    id: int
    image_name: str

class UploadImage(BaseModel):
    id: int
    name: str
    image: UploadFile

