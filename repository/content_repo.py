from abc import ABC, abstractmethod
from models.schemas import ContentRequest, ContentResponse
from typing import List, Optional
import json
from datetime import datetime

class ContentRepositoryInterface(ABC):
    """Interface pour la persistance du contenu (Dependency Inversion)"""

    @abstractmethod
    async def save_content(self, content: ContentResponse) -> bool:
        pass

    @abstractmethod
    async def get_unused_content(self) -> List[ContentResponse]:
        pass

    @abstractmethod
    async def save_content_with_request(self, content: ContentResponse, request: ContentRequest) -> bool:
        pass

class InMemoryContentRepository(ContentRepositoryInterface):
    """Repository en mémoire pour le développement (Single Responsibility)"""

    def __init__(self):
        self._storage: List[dict] = []

    async def save_content(self, content: ContentResponse) -> bool:
        """Sauvegarde le contenu généré"""
        content_dict = content.model_dump()
        content_dict["created_at"] = datetime.now().isoformat()
        self._storage.append(content_dict)
        return True

    async def get_unused_content(self) -> List[ContentResponse]:
        """Récupère le contenu non utilisé"""
        unused = [item for item in self._storage if item.get("used", 0) == 0]
        return [ContentResponse(**item) for item in unused]

    async def save_content_with_request(self, content: ContentResponse, request: ContentRequest) -> bool:
        """Sauvegarde avec informations de la requête"""
        content_dict = content.model_dump()
        content_dict["cible"] = request.cible.value
        content_dict["prospect_type"] = request.prospect_type.value
        content_dict["generation_date"] = request.date.isoformat()
        content_dict["created_at"] = datetime.now().isoformat()
        self._storage.append(content_dict)
        return True
    
class FileContentRepository(ContentRepositoryInterface):
    """Repository fichier JSON (peut remplacer InMemory - Liskov Substitution)"""

    def __init__(self, file_path: str = "content_storage.json"):
        self.file_path = file_path

    async def save_content(self, content: ContentResponse) -> bool:
        try:
            # Charger les données existantes
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []

            # Ajouter le nouveau contenu
            content_dict = content.model_dump()
            content_dict["created_at"] = datetime.now().isoformat()
            data.append(content_dict)

            # Sauvegarder
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception:
            return False

    async def get_unused_content(self) -> List[ContentResponse]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            unused = [item for item in data if item.get("used", 0) == 0]
            return [ContentResponse(**item) for item in unused]
        except FileNotFoundError:
            return []
