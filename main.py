
from fastapi import FastAPI
import model
from database import engine
from sqlalchemy.orm import Session
from routers import blog,user,authentication

app=FastAPI()

model.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

