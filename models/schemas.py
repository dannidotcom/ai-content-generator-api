from pydantic import BaseModel, Field, field_validator
from datetime import date
from enum import Enum
from typing import Literal
from datetime import datetime

class CibleEnum(str, Enum):
    LINKEDIN = "LinkedIn"
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    MAIL = "Mail"

class ProspectTypeEnum(str, Enum):
    PEU_QUALIFIE = "Peu qualifié"
    QUALIFIE = "Qualifié"
    HAUTEMENT_QUALIFIE = "Hautement qualifié"

class ContentRequest(BaseModel):
    cible: CibleEnum = Field(..., description="Canal marketing cible")
    prospect_type: ProspectTypeEnum = Field(..., description="Niveau de maturité du prospect")
    date: str = Field(..., description="Date de génération du contenu")
    @field_validator("date")
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La date doit être au format YYYY-MM-DD (ex: 2025-07-15)")
        return value

class ContentResponse(BaseModel):
    theme_general: str = Field(..., description="Ligne éditoriale principale")
    theme_hebdo: str = Field(..., description="Focus éditorial de la semaine")
    texte: str = Field(..., description="Contenu à publier")
    used: int = Field(default=0, description="Indicateur d'utilisation")
