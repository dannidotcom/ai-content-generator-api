from pydantic import BaseModel, Field, field_validator
from datetime import date
from enum import Enum
from typing import Literal, Union
from datetime import datetime
from datetime import datetime, date as dt_date

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

# class ContentRequests(BaseModel):
#     cible: CibleEnum = Field(..., description="Canal marketing cible")
#     prospect_type: ProspectTypeEnum = Field(..., description="Niveau de maturité du prospect")
#     date: str = Field(..., description="Date de génération du contenu")
#     @field_validator("date")
#     @classmethod
#     def validate_date_format(cls, value: str) -> str:
#         try:
#             datetime.strptime(value, "%Y-%m-%d")
#         except ValueError:
#             raise ValueError("La date doit être au format YYYY-MM-DD (ex: 2025-07-15)")
#         return value
class ContentRequest(BaseModel):
    cible: CibleEnum
    prospect_type: ProspectTypeEnum
    date: Union[str, dt_date] = Field(..., description="Date au format YYYY-MM-DD")

    @field_validator("date", mode="before")
    @classmethod
    def validate_date_format(cls, value) -> str:
        if isinstance(value, dt_date):
            return value.isoformat()
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("La date doit être au format YYYY-MM-DD (ex: 2025-07-15)")
            return value
        raise ValueError("Date invalide : doit être une chaîne YYYY-MM-DD ou un objet date.")
class ContentResponse(BaseModel):
    theme_general: str = Field(..., description="Ligne éditoriale principale")
    theme_hebdo: str = Field(..., description="Focus éditorial de la semaine")
    texte: str = Field(..., description="Contenu à publier")
    cible: CibleEnum = Field(..., description="Canal marketing cible")
    prospect_type: ProspectTypeEnum = Field(..., description="Niveau de maturité du prospect")
    generation_date: dt_date = Field(..., description="Date de génération du contenu")
    used: int = Field(default=0, description="Indicateur d'utilisation")
