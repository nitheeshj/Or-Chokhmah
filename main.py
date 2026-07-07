from fastapi import FastAPI
from routers import bible

app = FastAPI()

app.include_router(bible.router)


@app.get("/")
def home():
    return {"message": "Bible API is running"}

