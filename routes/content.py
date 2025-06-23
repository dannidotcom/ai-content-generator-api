from fastapi import APIRouter, HTTPException, Depends
from models.schemas import ContentRequest, ContentResponse
from services.content_ai import ContentGeneratorInterface, ContentGeneratorFactory
from repository.content_repo import ContentRepositoryInterface, InMemoryContentRepository

router = APIRouter(prefix="/api/v1", tags=["Content Generation"])

# Dependency Injection
def get_content_generator() -> ContentGeneratorInterface:
    return ContentGeneratorFactory.create_generator("openai")

def get_content_repository() -> ContentRepositoryInterface:
    return InMemoryContentRepository()

@router.post("/generate-content", response_model=ContentResponse)
async def generate_editorial_content(
    request: ContentRequest,
    generator: ContentGeneratorInterface = Depends(get_content_generator),
    repository: ContentRepositoryInterface = Depends(get_content_repository)
):
    """
    Génère du contenu éditorial personnalisé via IA
    
    - **cible**: Canal marketing (LinkedIn, Facebook, Instagram, TikTok, Mail)
    - **prospect_type**: Maturité commerciale (Peu qualifié, Qualifié, Hautement qualifié)
    - **date**: Date de génération du contenu
    
    Retourne un contenu éditorial avec thème général, thème hebdomadaire et texte.
    """
    try:
        # Générer le contenu via IA
        content = await generator.generate_content(request)
        
        # Sauvegarder le contenu généré
        await repository.save_content(content)
        
        return content
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du contenu: {str(e)}"
        )
