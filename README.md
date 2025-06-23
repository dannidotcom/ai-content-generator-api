# 🧠 Content Generator API

API REST construite avec **FastAPI** pour générer du contenu éditorial personnalisé à l’aide de **OpenAI**.

---

## 🚀 Installation

```bash
git clone https://github.com/dannidotcom/ai-content-generator-api.git
cd ai-content-generator-api
```

### 📦 Installer les dépendances

```bash
pip install -r requirements.txt
```

### ⚙️ Configuration des variables d’environnement

Copier le fichier exemple :

```bash
cp .env.example .env
```

Éditer le fichier `.env` pour y ajouter votre **clé API OpenAI** :

```env
OPENAI_API_KEY=sk-votre-cle-openai-ici
PORT=8000
OPENAI_MODEL=gpt-4o-mini
```

---

## 🏃 Lancement du serveur

```bash
uvicorn main:app --reload
```

L’API sera accessible à l’adresse : [http://localhost:8000](http://localhost:8000)

---

## 📖 Documentation interactive

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

---

## 🔗 Endpoint principal

### `POST /api/v1/generate-content`

Génère du contenu éditorial personnalisé via OpenAI.

#### 🟢 Exemple de requête

```json
{
  "cible": "LinkedIn",
  "prospect_type": "Qualifié",
  "date": "2025-01-15"
}
```

#### 🔵 Exemple de réponse

```json
{
  "theme_general": "Humaniser la marque via du contenu lifestyle",
  "theme_hebdo": "Mettre en avant les coulisses d'un projet client",
  "texte": "Cette semaine, publiez une série de photos...",
  "used": 0
}
```

---

## 📋 Valeurs acceptées

- **Cibles :** `LinkedIn`, `Facebook`, `Instagram`, `TikTok`, `Mail`
- **Types de prospects :** `Peu qualifié`, `Qualifié`, `Hautement qualifié`

---

## 🧪 Test rapide avec `curl`

Depuis un fichier :

```bash
curl -X POST "http://localhost:8000/api/v1/generate-content" \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

Ou directement en ligne :

```bash
curl -X POST "http://localhost:8000/api/v1/generate-content" \
  -H "Content-Type: application/json" \
  -d '{"cible": "Instagram", "prospect_type": "Qualifié", "date": "2025-07-15"}'
```

---

## 🔧 Diagnostic local

Vérifier la configuration d’OpenAI :

```bash
curl http://localhost:8000/debug/openai
```

---

## 🏗️ Architecture du projet

```
.
├── models/       # Schémas Pydantic
├── services/     # Logique métier (intégration OpenAI)
├── repository/   # Persistance éventuelle
├── routes/       # Endpoints REST
├── main.py       # Entrée principale de l'application
```

🧱 L’architecture suit les **principes SOLID** pour un code propre, testable et maintenable.

---

## 📫 Auteur

Développé par [@dannidotcom](https://github.com/dannidotcom)
