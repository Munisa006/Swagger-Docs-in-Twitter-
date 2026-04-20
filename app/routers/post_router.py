from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import Post, User
from app.schemas import PostCreate, PostOut

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post(
    "",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a post",
    description="Create a new tweet-like post for the authenticated user. Maximum 280 characters."
)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_post = Post(
        content=post_data.content,
        owner_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get(
    "",
    response_model=List[PostOut],
    summary="Get all posts",
    description="Return a list of all posts ordered from newest to oldest."
)
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.created_at.desc()).all()


@router.get(
    "/me",
    response_model=List[PostOut],
    summary="Get my posts",
    description="Return all posts created by the currently authenticated user."
)
def get_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Post)
        .filter(Post.owner_id == current_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )