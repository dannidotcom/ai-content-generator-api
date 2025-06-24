from datetime import date, datetime
import random
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from database.connexion import get_db
from models.schemas import CibleEnum, ContentRequest, ContentResponse, ProspectTypeEnum
from repository.conn_repo import DBContentRepository
from services.content_ai import ContentGeneratorInterface, ContentGeneratorFactory
from repository.content_repo import ContentRepositoryInterface, InMemoryContentRepository
from sqlalchemy.orm import Session

from services.excel_extract import ExcelExtractService

router = APIRouter(prefix="/api/v1", tags=["Content Generation"])

# Dependency Injection
def get_content_generator() -> ContentGeneratorInterface:
    return ContentGeneratorFactory.create_generator("openai")

def get_content_repository(db: Session = Depends(get_db)) -> ContentRepositoryInterface:
    return DBContentRepository(db)

@router.post("/generate-content", response_model=ContentResponse)
async def generate_editorial_content(
    request: ContentRequest,
    generator: ContentGeneratorInterface = Depends(get_content_generator),
    db: Session = Depends(get_db)
):
    """
    Génère du contenu éditorial personnalisé via IA

    - **cible**: Canal marketing (LinkedIn, Facebook, Instagram, TikTok, Mail)
    - **prospect_type**: Maturité commerciale (Peu qualifié, Qualifié, Hautement qualifié)
    - **date**: Date de génération du contenu

    Retourne un contenu éditorial avec thème général, thème hebdomadaire et texte.
    """
    try:
        repository = DBContentRepository(db)
        # Générer le contenu via IA
        content = await generator.generate_content(request)
        # Sauvegarder le contenu généré avec les infos de la requête
        await repository.save_content_with_request(content, request)

        return content
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du contenu: {str(e)}"
        )

@router.post("/generate-content-hebdo", response_model=List[ContentResponse])
async def generate_editorial_batch(
    date_: date,
    generator: ContentGeneratorInterface = Depends(get_content_generator),
    db: Session = Depends(get_db)
):
    """
    Génère automatiquement du contenu éditorial pour tous les canaux définis

    - Génère un contenu pour chaque **cible** (LinkedIn, Facebook, Instagram, TikTok, Mail)
    - Le **prospect_type** est choisi aléatoirement pour chaque cible
    - Tous les contenus sont sauvegardés en base

    Retourne une liste de contenus générés.
    """
    try:
        repository = DBContentRepository(db)
        results = []

        for cible in CibleEnum:
            prospect_type = random.choice(list(ProspectTypeEnum))

            request = ContentRequest(
                cible=cible,
                prospect_type=prospect_type,
                date=date_
            )

            content = await generator.generate_content(request)
            await repository.save_content_with_request(content, request)
            results.append(content)

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération de contenu hebdo : {str(e)}"
        )
@router.get("/getall-contents")
async def get_all_contents(
    cible: Optional[str] = Query(None),
    prospect_type: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Récupère tous les contenus avec pagination et filtres"""
    try:
        repository = DBContentRepository(db)
        contents = await repository.get_all_content(
            cible=cible,
            prospect_type=prospect_type,
            start_date=start_date,
            end_date=end_date
        )

        # Pagination
        total = len(contents)
        paginated_contents = contents[offset:offset + limit]

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "contents": [
                {
                    "id": content.id,
                    "cible": content.cible,
                    "prospect_type": content.prospect_type,
                    "generation_date": content.generation_date,
                    "theme_general": content.theme_general,
                    "theme_hebdo": content.theme_hebdo,
                    "texte": content.texte,
                    "used": content.used,
                    "created_at": content.created_at
                } for content in paginated_contents
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération: {str(e)}"
        )

@router.get("/extract-excel")
async def extract_content_to_excel(
    cible: Optional[str] = Query(None, description="Filtrer par cible"),
    prospect_type: Optional[str] = Query(None, description="Filtrer par type de prospect"),
    start_date: Optional[date] = Query(None, description="Date de début"),
    end_date: Optional[date] = Query(None, description="Date de fin"),
    db: Session = Depends(get_db)
):
    """
    Exporte les contenus générés vers un fichier Excel
    """
    try:
        repository = DBContentRepository(db)

        # Récupérer les contenus avec filtres
        contents = await repository.get_all_content(
            cible=cible,
            prospect_type=prospect_type,
            start_date=start_date,
            end_date=end_date
        )

        if not contents:
            raise HTTPException(status_code=404, detail="Aucun contenu trouvé")

        # Générer le fichier Excel
        excel_file = ExcelExtractService.extract_to_excel(contents)

        # Nom du fichier avec timestamp
        filename = f"contenus_editoriaux_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'export Excel: {str(e)}"
        )
