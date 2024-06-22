from database import metadata
from sqlalchemy import Table, Column, Integer, String

image = Table(
    "image",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("image_name", String, nullable=False),
)
