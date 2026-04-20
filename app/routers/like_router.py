from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import Like, Post, User
from app.schemas import LikeResponse

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)


@router.post(
    "/{post_id}",
    response_model=LikeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Like a post",
    description="Like a post by its ID. A user cannot like the same post twice."
)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = (
        db.query(Like)
        .filter(Like.user_id == current_user.id, Like.post_id == post_id)
        .first()
    )

    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this post")

    like = Like(user_id=current_user.id, post_id=post_id)
    db.add(like)
    db.commit()

    return {
        "message": "Post liked successfully",
        "post_id": post_id
    }


@router.delete(
    "/{post_id}",
    response_model=LikeResponse,
    summary="Unlike a post",
    description="Remove the authenticated user's like from a post."
)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    like = (
        db.query(Like)
        .filter(Like.user_id == current_user.id, Like.post_id == post_id)
        .first()
    )

    if not like:
        raise HTTPException(status_code=404, detail="Like not found for this user and post")

    db.delete(like)
    db.commit()

    return {
        "message": "Post unliked successfully",
        "post_id": post_id
    }