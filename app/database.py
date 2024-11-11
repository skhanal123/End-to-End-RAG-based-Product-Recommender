from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from pymongo import MongoClient
from pinecone import Pinecone
from llama_index.storage.chat_store.postgres import PostgresChatStore


## Section 1: POSTGRES connection setting in FastAPI: starts
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.postgresdb_username}:{settings.postgresdb_password}@{settings.postgresdb_hostname}:{settings.postgresdb_port}/{settings.postgresdb_dbname}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## Section 1: ends


## Section 2: Mongodb connection and client creation: starts
class MongoEngine:
    client = MongoClient(settings.mongodb_uri)


## Section 2: ends


## Section 3: Pinecone vector database connection and client creation: starts
class PineconeEngine:
    client = Pinecone(api_key=settings.pinecone_api_key)


## Section 3: ends


## Section 4: Postgres chat store connection and client creation: starts

chat_store = PostgresChatStore.from_uri(
    uri=f"postgresql+asyncpg://{settings.postgresdb_username}:{settings.postgresdb_password}@{settings.postgresdb_hostname}:{settings.postgresdb_port}/{settings.postgresdb_dbname}",
)
## Section 4: ends
