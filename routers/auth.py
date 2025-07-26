from fastapi import APIRouter,HTTPException,status,Depends
from .. import schemas,database,oauth2,models,hashing,token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from ..repository import auth

router=APIRouter(tags=['AUTHS'])

get_db = database.get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post('/auth/register',status_code=status.HTTP_201_CREATED,response_model=schemas.Showuser)
def create_user(request:schemas.User,db : Session = Depends(get_db)):
    return auth.create_user(request,db)

@router.post('/auth/login')
def login(request : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email== request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Incorrect credentials')
    if not hashing.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'incorrect password')
    access_token = token.create_access_token(data={"sub": user.email})
    return {'access_token':access_token, 'token_type':"bearer"}

@router.get('/auth/me', response_model=schemas.Showuser)
def get_user(current_user: schemas.User = Depends(oauth2.get_current_user),):
    return current_user

