from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.content import router as content_router
import os
from dotenv import load_dotenv
import uvicorn
from database.connexion import Base, engine

load_dotenv()

app = FastAPI(
    title="Content Generator API",
    description="API REST pour générer du contenu éditorial personnalisé via IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Créer les tables
Base.metadata.create_all(bind=engine)

# Inclusion des routes
app.include_router(content_router)

@app.get("/")
async def root():
    return {
        "message": "Content Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug/openai")
async def debug_openai():
    """Route de diagnostic pour vérifier la configuration OpenAI"""
    api_key = os.getenv("OPENAI_API_KEY")
    return {
        "openai_configured": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0,
        "api_key_preview": f"{api_key[:8]}..." if api_key and len(api_key) > 8 else "Non configurée"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
