from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/likes", tags=["Likes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/me", response_model=List[schemas.PostOut])
def get_my_liked_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    likes = db.query(models.Like).filter(
        models.Like.user_id == current_user.id
    ).all()

    post_ids = [like.post_id for like in likes]

    posts = db.query(models.Post).filter(
        models.Post.id.in_(post_ids)
    ).all()

    return posts