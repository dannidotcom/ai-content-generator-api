from sqlalchemy.orm import Session
from database.models import GeneratedContent
from repository.content_repo import ContentRepositoryInterface
from models.schemas import ContentResponse, ContentRequest
from typing import List, Optional
from datetime import datetime, date

class DBContentRepository(ContentRepositoryInterface):
    """Repository PostgreSQL (Single Responsibility)"""

    def __init__(self, db: Session):
        self.db = db

    async def save_content(self, content: ContentResponse, request: ContentRequest = None) -> bool:
        """Sauvegarde le contenu généré en base"""
        try:
            db_content = GeneratedContent(
                cible=request.cible.value if request else "Unknown",
                prospect_type=request.prospect_type.value if request else "Unknown",
                generation_date=request.date if request else date.today(),
                theme_general=content.theme_general,
                theme_hebdo=content.theme_hebdo,
                texte=content.texte,
                used=content.used
            )

            self.db.add(db_content)
            self.db.commit()
            self.db.refresh(db_content)
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Erreur sauvegarde PostgreSQL: {str(e)}")
            return False

    async def save_content_with_request(self, content: ContentResponse, request: ContentRequest) -> bool:
        """Sauvegarde le contenu généré avec les informations de la requête"""
        try:
            db_content = GeneratedContent(
                cible=request.cible.value,
                prospect_type=request.prospect_type.value,
                generation_date=request.date,
                theme_general=content.theme_general,
                theme_hebdo=content.theme_hebdo,
                texte=content.texte,
                used=content.used
            )

            self.db.add(db_content)
            self.db.commit()
            self.db.refresh(db_content)
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Erreur sauvegarde PostgreSQL avec requête: {str(e)}")
            return False
        
    async def get_unused_content(self) -> List[ContentResponse]:
        """Récupère le contenu non utilisé"""
        try:
            contents = self.db.query(GeneratedContent).filter(
                GeneratedContent.used == 0
            ).all()

            return [
                ContentResponse(
                    theme_general=content.theme_general,
                    theme_hebdo=content.theme_hebdo,
                    texte=content.texte,
                    used=content.used
                ) for content in contents
            ]
        except Exception:
            return []

    async def get_all_content(self,
                            cible: Optional[str] = None,
                            prospect_type: Optional[str] = None,
                            start_date: Optional[date] = None,
                            end_date: Optional[date] = None) -> List[GeneratedContent]:
        """Récupère tout le contenu avec filtres optionnels"""
        query = self.db.query(GeneratedContent)

        if cible:
            query = query.filter(GeneratedContent.cible == cible)
        if prospect_type:
            query = query.filter(GeneratedContent.prospect_type == prospect_type)
        if start_date:
            query = query.filter(GeneratedContent.generation_date >= start_date)
        if end_date:
            query = query.filter(GeneratedContent.generation_date <= end_date)

        return query.order_by(GeneratedContent.created_at.desc()).all()

    async def mark_as_used(self, content_id: int) -> bool:
        """Marque un contenu comme utilisé"""
        try:
            content = self.db.query(GeneratedContent).filter(
                GeneratedContent.id == content_id
            ).first()

            if content:
                content.used = 1
                self.db.commit()
                return True
            return False
        except Exception:
            self.db.rollback()
            return False
