from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app.models import Follow, User
from app.schemas import FollowResponse, UserProfileResponse, FollowedUserOut

router = APIRouter(
    prefix="/follows",
    tags=["Follows"]
)


@router.post(
    "/{target_user_id}",
    response_model=FollowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Follow a user",
    description="Follow another user by their user ID. A user cannot follow themselves or follow the same user twice."
)
def follow_user(
    target_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id == target_user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    target_user = db.query(User).filter(User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    existing_follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == target_user_id
        )
        .first()
    )

    if existing_follow:
        raise HTTPException(status_code=400, detail="You already follow this user")

    follow = Follow(
        follower_id=current_user.id,
        following_id=target_user_id
    )

    db.add(follow)
    db.commit()

    return {
        "message": "User followed successfully",
        "target_user_id": target_user_id
    }


@router.delete(
    "/{target_user_id}",
    response_model=FollowResponse,
    summary="Unfollow a user",
    description="Stop following a user by their user ID."
)
def unfollow_user(
    target_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == target_user_id
        )
        .first()
    )

    if not follow:
        raise HTTPException(status_code=404, detail="You are not following this user")

    db.delete(follow)
    db.commit()

    return {
        "message": "User unfollowed successfully",
        "target_user_id": target_user_id
    }


@router.get(
    "/profile/{user_id}",
    response_model=UserProfileResponse,
    summary="Get user profile info",
    description="Return a user profile with followers count, following count, and posts count."
)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers_count = db.query(Follow).filter(Follow.following_id == user_id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user_id).count()
    posts_count = len(user.posts)

    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": posts_count
    }


@router.get(
    "/me",
    response_model=List[FollowedUserOut],
    summary="Get users I follow",
    description="Return a list of users followed by the currently authenticated user."
)
def get_users_i_follow(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    follows = (
        db.query(Follow)
        .filter(Follow.follower_id == current_user.id)
        .all()
    )

    followed_user_ids = [follow.following_id for follow in follows]

    if not followed_user_ids:
        return []

    users = (
        db.query(User)
        .filter(User.id.in_(followed_user_ids))
        .all()
    )

    return users