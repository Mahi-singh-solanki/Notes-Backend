from sqlalchemy.orm import Session
from .. import schemas,database,models,hashing,token
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

def create_user(request :schemas.User,db : Session):
    new_user = models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    


    