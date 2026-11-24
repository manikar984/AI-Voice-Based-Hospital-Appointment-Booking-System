from fastapi import APIRouter, HTTPException, status

from appointments_db import get_user_by_username

from schemas import (
    LoginRequest,
    Token
)

from security import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/login",
    response_model=Token,
    summary="User Login",
    description="Authenticate a user and return a JWT access token."
)
def login(login_data: LoginRequest):

    user = get_user_by_username(login_data.username)

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(
        login_data.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {
            "sub": user["username"],
            "role": user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"]
    }