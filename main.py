from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import APP_CONFIG, SECURITY_CONFIG
from db.database import engine, Base
from api.v1 import api_router

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_CONFIG["title"],
    description=APP_CONFIG["description"],
    version=APP_CONFIG["version"]
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À configurer selon l'environnement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes API
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bienvenue sur FOFAL ERP API"}