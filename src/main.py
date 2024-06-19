from fastapi import FastAPI

# from auth.base_config import auth_backend, fastapi_users, current_user
# from auth.models import User
# from auth.schemas import UserRead, UserCreate
from image.router import router as router_image

app = FastAPI(
    title="Images App"
)

# app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth",
#     tags=["Auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Auth"],
# )

app.include_router(router_image)


