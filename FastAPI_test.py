from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import uuid
import httpx
import uvicorn

app = FastAPI()

# Словарь, хранящий короткие URL
short_url_db = {}

class URLRequest(BaseModel):
    url: HttpUrl

@app.get("/fetch-data")
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
    return response.json()

@app.post("/", status_code=201)
async def shorten_url(request: URLRequest):
    short_id = str(uuid.uuid4())[:8]
    short_url_db[short_id] = request.url
    return {"short_url": f"/{short_id}"}

@app.get("/{short_id}", status_code=307)
async def get_original_url(short_id: str):
    if short_id not in short_url_db:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {"Location": short_url_db[short_id]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
