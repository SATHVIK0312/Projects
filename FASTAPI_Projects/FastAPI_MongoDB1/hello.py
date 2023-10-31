# hello.py
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route that responds to the root URL (localhost)
@app.get("/hello")
async def read_root():
    return {"message": "Hello, World!"}
