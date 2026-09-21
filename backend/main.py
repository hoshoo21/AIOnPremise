from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title = "Chose your own adventure game api0",
    
    
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_method = ["*"],
    allow_headers = ["*"]
)


