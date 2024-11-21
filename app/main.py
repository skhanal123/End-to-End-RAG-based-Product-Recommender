from fastapi import FastAPI
from .routers import user, auth, chat
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"message": "Backend test"}
