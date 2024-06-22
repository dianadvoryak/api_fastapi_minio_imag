import os
import shutil
import uuid

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi import UploadFile
from minio import Minio
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import image as image_model

minio_client = Minio("127.0.0.1:9000",
                     access_key="miniominiominio",
                     secret_key="miniominiominio",
                     secure=False
                     )

bucket_name = "images"

router = APIRouter(
    prefix="/image",
    tags=["Image"]
)


@router.get("/images")
def get_base_page():
    objects = minio_client.list_objects(bucket_name, recursive=True)
    return objects


@router.get("/images/{get_name}")
async def get_images(get_name: str, session: AsyncSession = Depends(get_async_session)):

    try:
        query = select(image_model.c.image_name).where(image_model.c.name == get_name)
        result = await session.execute(query)
        image_name = str(result.scalars().first())
        if not image_name:
            raise HTTPException(status_code=500, detail={
                "status": "not found",
                "data": None,
                "details": None
            })
        response = minio_client.get_object(bucket_name, image_name)
        data = response.read()
        response.close()
        response.release_conn()
        return Response(content=data, media_type="image/png")

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })



@router.post("/upload/")
async def create_image(image: UploadFile, name: str,
                       session: AsyncSession = Depends(get_async_session)):
    image_name = f"{uuid.uuid4()}" + ".png"
    image_path = "../store/" + image_name

    try:
        query = (
            insert(image_model).
            values(name=name, image_name=image_name)
        )
        await session.execute(query)
        await session.commit()
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

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


@router.post("/remove/{get_name}")
async def remove_image(get_name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(image_model.c.image_name).where(image_model.c.name == get_name)
        result = await session.execute(query)
        image_name = str(result.scalars().first())

        minio_client.remove_object(bucket_name, image_name)
        if not image_name:
            raise HTTPException(status_code=500, detail={
                "status": "not found",
                "data": None,
                "details": None
            })
        minio_client.remove_object(bucket_name, image_name)
        query = delete(image_model).where(image_model.c.name == get_name)
        await session.execute(query)
        return {
            "status": "success",
            "data": "image remove",
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


