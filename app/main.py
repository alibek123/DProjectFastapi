import os
from fastapi import FastAPI
from .routers import meals, categories, users, auth, cart, orders
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = ["*"]
BASEDIR = os.path.dirname(__file__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],

)


@app.get("/")
async def root():
    return {"message": "Hello World from CI/CD pipeline"}


app.include_router(meals.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.mount("/static", StaticFiles(directory=BASEDIR + "/statics"), name="static")
