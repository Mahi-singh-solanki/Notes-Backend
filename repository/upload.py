from transformers import pipeline
from fastapi import FastAPI,UploadFile,File,HTTPException,status,BackgroundTasks,Depends
from sqlalchemy.orm import Session
from typing import Annotated
from PIL import Image
from pytesseract import pytesseract
import io,os
import fitz
from .. import models,schemas,database,oauth2

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def summarize_text(text: str,user_id: int):
    db = database.SessionLocal()

    try:
        # if len(text) > 1000:
            text = text[:1000]
            summary_output = summarizer(text, max_length=130, min_length=30, do_sample=False)
            summary = summary_output[0]['summary_text']
            new_summary=models.Summary(original_text= text,summary_text=summary,user_id=user_id)
            db.add(new_summary)
            db.commit()
            db.refresh(new_summary)
            return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
    finally:
        db.close()



def summarize_file(db:Session,upload_file:int,current_user: models.User):
    uploaded_file=db.query(models.Upload).filter(models.Upload.id==upload_file).first()

    summarize_text(uploaded_file.text,current_user.id)
    
    return {'summarized':'success'}
    

def up_file(current_user,uploadfile:UploadFile = File(description="A file read as UploadFile")):   
    db = database.SessionLocal()
    filename = uploadfile.filename.lower()
    if filename.endswith((".png", ".jpg", ".jpeg")):
        image_bytes = uploadfile.file.read()
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        file_type = "image"

    elif filename.endswith(".pdf"):
        pdf_bytes = uploadfile.file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        file_type = "pdf"

    else:
        return {"error": "Unsupported file type. Please upload a PDF or image file."}
    try:
        new_text=models.Upload(text= text,user_id=current_user.id)
        db.add(new_text)
        db.commit()
        db.refresh(new_text)
    finally:
        db.close()
    


    return {
        "filename": uploadfile.filename,
        "file_type": file_type,
        "extracted_text": len(text)
    }