from database.connexion import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func

class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    cible = Column(String(50), nullable=False, index=True)
    prospect_type = Column(String(50), nullable=False, index=True)
    generation_date = Column(DateTime, nullable=False, index=True)
    theme_general = Column(Text, nullable=False)
    theme_hebdo = Column(Text, nullable=False)
    texte = Column(Text, nullable=False)
    used = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
