from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
import sql_models

sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SchoolSphere API")

@app.get("/")
def read_root():
    return {"message": "Welcome to SchoolSphere API"}

# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}
