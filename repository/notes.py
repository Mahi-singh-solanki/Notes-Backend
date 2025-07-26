from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from .. import models,database
from transformers import pipeline

db=database.get_db


note_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1
)
def get_notes(db:Session,upload_id,current_user):
    summary_entry=db.query(models.Upload).filter(models.Upload.id==upload_id,models.Upload.user_id == current_user.id).first()

    if not summary_entry:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    summary = summary_entry.text
    prompt = f"Generate 5 key study notes from this summary:\n{summary}"
    output = note_generator(prompt, max_new_tokens=256, do_sample=False)[0]['generated_text']
    notes = [line.strip("12345.:- ").strip() for line in output.split("\n") if line.strip()]
    Notes=models.Note(user_id=current_user.id,notes="\n".join(notes))
    db.add(Notes)
    db.commit()
    db.refresh(Notes)
    return 'Note generated'
    

        
        
    


