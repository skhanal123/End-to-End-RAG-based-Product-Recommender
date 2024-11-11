from pydantic_settings import BaseSettings, SettingsConfigDict
import os

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_userprofile: str
    mongodb_userprofile_collection: str
    scraper_api_token: str
    pinecone_index: str
    pinecone_api_key: str
    openai_api_key: str
    postgresdb_hostname: str
    postgresdb_port: int
    postgresdb_password: str
    postgresdb_dbname: str
    postgresdb_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
