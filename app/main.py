from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.post import router as post_router
from app.routers.auth import router as auth_router


app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(post_router, prefix="/post", tags=["Post"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "okay"}