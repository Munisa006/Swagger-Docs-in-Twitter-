from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.auth_router import router as auth_router
from app.routers.post_router import router as post_router
from app.routers.like_router import router as like_router
from app.routers.follow_router import router as follow_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Twitter API",
    description="A simple Twitter-like backend built with FastAPI.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Mini Twitter API is running"}

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(follow_router)