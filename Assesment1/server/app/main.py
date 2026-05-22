from fastapi import FastAPI
from app.services import get_posts
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:5173",   
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/posts')
def posts():

    data = get_posts()

    return {
        "success":True,
        "data":data
    }