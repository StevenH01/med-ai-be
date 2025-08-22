# app/main.py
from fastapi import FastAPI
from app.routers import ingest
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(ingest.router, prefix="/api")
