from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth,upload,notes

models.Base.metadata.create_all(engine)

app=FastAPI()

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(notes.router)