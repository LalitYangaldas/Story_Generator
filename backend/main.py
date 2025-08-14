from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from routers import story, job
from db.database import create_tables

create_tables()

app = FastAPI(
    title="Choose your own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/",
    redoc_url="/redoc",
)

# Define a root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Choose your own Adventure Game API!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)