# Content Generator API

API REST FastAPI pour générer du contenu éditorial personnalisé via OpenAI.

## 🚀 Installation

\`\`\`bash
# Cloner le projet
git clone https://github.com/dannidotcom/ai-content-generator-api.git
cd content-generator-api

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et ajouter votre clé OpenAI
\`\`\`

## ⚙️ Configuration

Créer un fichier \`.env\` avec :

\`\`\`env
OPENAI_API_KEY=sk-votre-cle-openai-ici
PORT=8000
OPENAI_MODEL=gpt-4o-mini
\`\`\`

## 🏃 Lancement

\`\`\`bash
uvicorn main:app --reload
\`\`\`

L'API sera disponible sur : http://localhost:8000

## 📖 Documentation

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔗 Endpoint Principal

### POST /api/v1/generate-content

Génère du contenu éditorial personnalisé.

**Request :**
\`\`\`json
{
  "cible": "LinkedIn",
  "prospect_type": "Qualifié",
  "date": "2025-01-15"
}
\`\`\`

**Response :**
\`\`\`json
{
  "theme_general": "Humaniser la marque via du contenu lifestyle",
  "theme_hebdo": "Mettre en avant les coulisses d'un projet client",
  "texte": "Cette semaine, publiez une série de photos...",
  "used": 0
}
\`\`\`

## 📋 Valeurs Acceptées

**Cibles :** LinkedIn, Facebook, Instagram, TikTok, Mail

**Types de prospects :** Peu qualifié, Qualifié, Hautement qualifié

## 🧪 Test Rapide

\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/generate-content" \
  -H "Content-Type: application/json" \
  -d @example_request.json
\`\`\`

## 🔧 Diagnostic

Vérifier la configuration OpenAI :
\`\`\`bash
curl http://localhost:8000/debug/openai
\`\`\`

## 🏗️ Architecture

- **models/** : Schémas Pydantic
- **services/** : Logique métier (OpenAI)
- **repository/** : Persistance des données
- **routes/** : Endpoints REST

Respecte les principes SOLID pour une architecture maintenable.
