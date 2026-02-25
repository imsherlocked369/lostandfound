from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.user import UserRepository
from app.services.user import UserService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def userServiceRepoInjected(db: Session = Depends(get_db)) -> UserService:
    userRepository = UserRepository(db)
    return UserService(userRepository)
