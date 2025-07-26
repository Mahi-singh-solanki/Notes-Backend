from fastapi import APIRouter,UploadFile,File,Depends,HTTPException,status
from typing import Annotated,List
from ..repository import upload
from .. import schemas,oauth2,database,models
from sqlalchemy.orm import Session

router = APIRouter()
get_db = database.get_db

@router.post('/upload',tags=['uploads'])
def uploadfile(uploadfile:Annotated[UploadFile,File(description="A file read as UploadFile")],current_user : schemas.User = Depends(oauth2.get_current_user)):
    return upload.up_file(current_user,uploadfile)

@router.get('/upload/user',response_model=List[schemas.Upload],tags=['uploads'])
def get_user_text(db: Session = Depends(get_db),current_user: schemas.Showuser = Depends(oauth2.get_current_user)):
    uploads = db.query(models.Upload).filter(models.Upload.user_id == current_user.id).all()
    return uploads

@router.get('/upload/{id}',response_model=schemas.Upload,tags=['uploads'])
def get_text(id,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    upload = db.query(models.Upload).filter(models.Upload.id==id).first()
    if not upload:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")
    return upload

@router.post('/summarize/{upload_id}',tags=['summaries'])
def summarize(upload_id,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return upload.summarize_file(db,upload_id,current_user)

@router.get('/summarize/users',response_model=List[schemas.Summary],tags=['summaries'])
def get_summaries(db: Session = Depends(get_db),current_user: schemas.Showuser = Depends(oauth2.get_current_user)):
    summaries=db.query(models.Summary).filter(models.Summary.user_id==current_user.id).all()
    return summaries


@router.get('/summarize/{summary_id}',tags=['summaries'])
def summarize(summary_id,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    summary=db.query(models.Summary).filter(models.Summary.id==summary_id).first()
    return {'summary':summary.summary_text}
 




