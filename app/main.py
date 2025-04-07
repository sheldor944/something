import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from db import Base, engine
from routers import router
from middleware import log_middleware

app = FastAPI()

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware,dispatch=log_middleware)

os.makedirs("media", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
def root():
        return{
                "Intro":"Welcome to  my Thesis backendd"
        }

#routing
app.include_router(router)

