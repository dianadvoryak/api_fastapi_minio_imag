import os
import shutil
import uuid

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi import UploadFile
from minio import Minio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import image as image_model

minio_client = Minio("127.0.0.1:9000",
                     access_key="miniominiominio",
                     secret_key="miniominiominio",
                     secure=False
                     )

router = APIRouter(
    prefix="/image",
    tags=["Image"]
)


@router.get("/image")
def get_base_page(request: Request):
    pass


@router.post("/uploadfile/")
async def create_upload_file(image: UploadFile, name: str,
                             session: AsyncSession = Depends(get_async_session)):
    image_name = f"{uuid.uuid4()}" + ".png"
    image_path = "../store/" + image_name

    # query = (
    #     insert(image_model).values(name=name, image_name=image_name)
    # )
    # res = await session.execute(query)
    # await session.commit()
    # return image_path
    try:
        query = (
            insert(image_model).
            values(name=name, image_name=image_name)
        )
        await session.execute(query)
        await session.commit()
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        bucket_name = "images"
        minio_client.fput_object(
            bucket_name, image_name, image_path,
        )
        os.remove(image_path)
        return {
            "status": "success",
            "data": "image uploaded",
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
