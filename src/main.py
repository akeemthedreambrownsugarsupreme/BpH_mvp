import sys
import os
from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.routes import rental, commercial

app = FastAPI()

app.include_router(rental.router, prefix="/rental")
# app.include_router(commercial.router, prefix="/commercial")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)