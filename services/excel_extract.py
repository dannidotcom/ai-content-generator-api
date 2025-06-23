import pandas as pd
from io import BytesIO
from typing import List
from database.models import GeneratedContent
from datetime import datetime

class ExcelExtractService:
    """Service d'extraction Excel (Single Responsibility)"""

    @staticmethod
    def extract_to_excel(contents: List[GeneratedContent]) -> BytesIO:
        """Extrait les contenus vers un fichier Excel"""

        # Préparer les données
        data = []
        for content in contents:
            data.append({
                'ID': content.id,
                'Cible': content.cible,
                'Type Prospect': content.prospect_type,
                'Date Génération': content.generation_date.strftime('%Y-%m-%d'),
                'Thème Général': content.theme_general,
                'Thème Hebdomadaire': content.theme_hebdo,
                'Texte': content.texte,
                'Utilisé': 'Oui' if content.used == 1 else 'Non',
                'Créé le': content.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Créer le DataFrame
        df = pd.DataFrame(data)

        # Créer le fichier Excel en mémoire
        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Feuille principale avec tous les contenus
            df.to_excel(writer, sheet_name='Tous les contenus', index=False)

            # Feuille par cible
            for cible in df['Cible'].unique():
                cible_df = df[df['Cible'] == cible]
                sheet_name = f'Contenu {cible}'[:31]  # Limite Excel
                cible_df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Feuille statistiques
            stats_data = {
                'Métrique': [
                    'Total contenus',
                    'Contenus utilisés',
                    'Contenus non utilisés',
                    'Nombre de cibles',
                    'Nombre de types prospects'
                ],
                'Valeur': [
                    len(df),
                    len(df[df['Utilisé'] == 'Oui']),
                    len(df[df['Utilisé'] == 'Non']),
                    df['Cible'].nunique(),
                    df['Type Prospect'].nunique()
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='Statistiques', index=False)

        output.seek(0)
        return output
