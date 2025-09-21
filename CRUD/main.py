from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
from . import schemas, models                
from .database import engine, SessionLocal   
from .hashing import Hash                    
from sqlalchemy.orm import Session
from .Routers import blog, user, authentication 


app = FastAPI(title="Blog API")

models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)







