from abc import ABC, abstractmethod
from models.schemas import ContentRequest, ContentResponse
from openai import OpenAI
import json
import os, re

class ContentGeneratorInterface(ABC):
    """Interface pour la génération de contenu (Interface Segregation)"""

    @abstractmethod
    async def generate_content(self, request: ContentRequest) -> ContentResponse:
        pass

class OpenAIContentGenerator(ContentGeneratorInterface):
    """Générateur de contenu utilisant OpenAI (Single Responsibility)"""

    def __init__(self, api_key: str = None):
        print("Initialisation du générateur de contenu OpenAI")
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    async def generate_content(self, request: ContentRequest) -> ContentResponse:
        """Génère du contenu éditorial via OpenAI"""

        prompt = self._build_prompt(request)

        try:
            if not self.client.api_key:
                raise ValueError("Clé API OpenAI non configurée")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un expert en marketing digital et création de contenu éditorial. Réponds uniquement en JSON valide."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            content_text = response.choices[0].message.content.strip()
            # Nettoyage du texte pour enlever les balises de code
            if content_text.startswith("```"):
                content_text = re.sub(r"^```(?:json)?\s*", "", content_text)
                content_text = re.sub(r"\s*```$", "", content_text)

            content_json = json.loads(content_text)

            return ContentResponse(
                theme_general=content_json["theme_general"],
                theme_hebdo=content_json["theme_hebdo"],
                texte=content_json["texte"],
                used=0
            )

        except json.JSONDecodeError as e:
            print(f"Erreur JSON: {str(e)}")
            return self._get_fallback_content(request)
        except Exception as e:
            print(f"Erreur OpenAI: {str(e)}")
            return self._get_fallback_content(request)

    def _build_prompt(self, request: ContentRequest) -> str:
        """Construit le prompt pour OpenAI"""
        return f"""
    Génère du contenu éditorial pour:
    - Cible: {request.cible.value}
    - Type de prospect: {request.prospect_type.value}
    - Date: {request.date}

    Réponds uniquement avec un JSON contenant:
    {{
        "theme_general": "ligne éditoriale principale adaptée à {request.cible.value}",
        "theme_hebdo": "focus éditorial spécifique pour la semaine du {request.date}",
        "texte": "contenu concret à publier, adapté au niveau {request.prospect_type.value}"
    }}

    Le contenu doit être pertinent pour {request.prospect_type.value} sur {request.cible.value}.
    """

    def _get_fallback_content(self, request: ContentRequest) -> ContentResponse:
        """Contenu de secours en cas d'erreur OpenAI"""
        return ContentResponse(
            theme_general=f"Contenu {request.cible.value} pour {request.prospect_type.value}",
            theme_hebdo=f"Focus hebdomadaire du {request.date}",
            texte=f"Contenu générique pour {request.cible.value} - {request.prospect_type.value}",
            used=0
        )

class ContentGeneratorFactory:
    """Factory pour créer des générateurs de contenu (Open/Closed Principle)"""

    @staticmethod
    def create_generator(generator_type: str = "openai") -> ContentGeneratorInterface:
        if generator_type == "openai":
            return OpenAIContentGenerator()
        else:
            raise ValueError(f"Type de générateur non supporté: {generator_type}")
