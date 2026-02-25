from fastapi import APIRouter, Depends, HTTPException, status

from app.constant.error import AuthError
from app.dependencies.userDependency import userServiceRepoInjected
from app.schemas.user import AuthTokenResponse, UserCreate, UserLogin, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate, userService: UserService = Depends(userServiceRepoInjected)
):
    try:
        return userService.create_user(payload)
    except ValueError as e:
        if str(e) == AuthError.EMAIL_ALREADY_EXISTS:
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=AuthTokenResponse)
def login(payload: UserLogin, userService: UserService = Depends(userServiceRepoInjected)):
    try:
        token = userService.login(payload.email, payload.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
