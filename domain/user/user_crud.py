from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from model import User
from passlib.context import CryptContext

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username = user_create.username,
                   password = pwd_context.hash(user_create.password1),
                   email = user_create.email)
    db.add(db_user)
    db.commit()

#비번 암호화 구현
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_existing_user(db: Session, user_create):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

