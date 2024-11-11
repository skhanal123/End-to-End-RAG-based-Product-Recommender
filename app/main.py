from fastapi import FastAPI
from .routers import user, auth, chat
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"message": "Backend test"}
