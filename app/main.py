from fastapi import FastAPI
from .routers import meals, categories, users, auth
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],

)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(meals.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(auth.router)
