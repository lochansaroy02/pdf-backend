# backend/app/main.py
from fastapi import FastAPI
from app.api.endpoints import upload, ask
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# cors error fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(upload.router, prefix="/api")
app.include_router(ask.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}
