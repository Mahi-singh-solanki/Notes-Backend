from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from .. import models,database
from transformers import pipeline

db=database.get_db


qa_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1
)

def create_questions(db:Session,upload_id,current_user):
    summary_entry=db.query(models.Note).filter(models.Note.id==upload_id,models.Note.user_id == current_user.id).first()
    if not summary_entry:
        raise HTTPException(status_code=404, detail="Summary not found")
    summary = summary_entry.notes
    prompt = (
            f"Generate 5 key study questions from this summary:\n{summary}"    
    )

    output = qa_generator(prompt, max_new_tokens=256, do_sample=False)[0]['generated_text']
    questions = [line.strip("12345.:- ").strip() for line in output.split("\n") if line.strip()]
    new_quiz=models.Quiz(quizes= "\n".join(questions),user_id=current_user.id)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)    
    return {
        "title": "Generated Quiz",
    }
           
        
        
        

    


    