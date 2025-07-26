from fastapi import APIRouter,Depends
from typing import List
from sqlalchemy.orm import Session
from .. import database,oauth2,schemas,models
from ..repository import notes,quiz

router=APIRouter(tags=['notes'])

get_db=database.get_db

@router.post('/notes/{upload_id}')
def generate_notes(upload_id:int,db:Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return notes.get_notes(db,upload_id,current_user)

@router.get('/notes/users',response_model=List[schemas.Note])
def get_notes_all(db: Session = Depends(get_db),current_user: schemas.Showuser = Depends(oauth2.get_current_user)):
    notes=db.query(models.Note).filter(models.Note.user_id==current_user.id).all()
    return notes

@router.get('/notes/{note_id}')
def get_notes(note_id:int,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    notes=db.query(models.Note).filter(models.Note.id==note_id).first()
    return {'title':'AI-Generated Notes','notes':notes.notes}

@router.post('/questions/{upload_id}')
def create_questions(upload_id:int,db:Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    return quiz.create_questions(db,upload_id,current_user)

@router.get('/questions/users',response_model=List[schemas.Quiz])
def get_quizes_all(db: Session = Depends(get_db),current_user: schemas.Showuser = Depends(oauth2.get_current_user)):
    quizes=db.query(models.Quiz).filter(models.Quiz.user_id==current_user.id).all()
    return quizes

@router.get('/questions/{quiz_id}')
def get_quizes(quiz_id:int,db : Session = Depends(get_db),current_user : schemas.User = Depends(oauth2.get_current_user)):
    quizes=db.query(models.Quiz).filter(models.Quiz.id==quiz_id).first()
    return {'title':'AI-Generated Quizes','quizeses':quizes.quizes}