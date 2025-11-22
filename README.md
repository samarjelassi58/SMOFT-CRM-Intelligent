# SMOFT CRM Intelligent

Un CRM qui comprend vraiment vos clients et vous aide à prioriser vos actions commerciales.

## À propos du projet

Vous connaissez ce moment où vous regardez votre liste de prospects et vous vous demandez par qui commencer ? C'est exactement le problème que nous avons voulu résoudre.

SMOFT CRM Intelligent analyse automatiquement le comportement de vos clients et vous dit clairement qui est prêt à acheter maintenant, qui a besoin d'un peu plus d'attention, et qui peut attendre. Plus besoin de deviner - le système fait le tri pour vous grâce à l'intelligence artificielle.

## Ce que ça fait pour vous

- **Note vos prospects automatiquement** : Chaque client reçoit un score de 0 à 100 selon son potentiel
- **Classe vos contacts en trois groupes** : Chauds (à appeler maintenant), Tièdes (à relancer cette semaine), Froids (peuvent attendre)
- **Comprend le comportement de vos clients** : Regarde qui ouvre vos emails, visite votre site, et achète chez vous
- **Vous dit exactement quoi faire** : "Appelle celui-là maintenant !" ou "Envoie un email à celui-ci"
- **S'intègre facilement** : Une simple API REST que vous pouvez brancher à votre système existant
- **Traite plusieurs clients d'un coup** : Donnez-lui toute votre base de données, il la traite en quelques secondes
- **Documentation claire** : Une interface interactive pour tester sans coder

## Architecture

```
PFE_SMOFT_CRM_Intelligent/
│
├── demo/
│   ├── api.py                 # API REST FastAPI
│   ├── scoring_model.py       # Modèle de scoring ML
│   ├── test_api.py           # Tests de l'API
│   └── requirements.txt      # Dépendances Python
│
├── web/
│   ├── index.html            # Interface web
│   └── index.php             # Backend PHP
│
└── start_server.bat          # Script de démarrage
```

## Ce qu'il y a sous le capot

- **Backend API** : FastAPI et Uvicorn (rapides et modernes)
- **Intelligence artificielle** : scikit-learn avec Random Forest (fiable et éprouvé)
- **Traitement de données** : pandas et numpy (les standards de l'industrie)
- **Interface web** : HTML et JavaScript simples
- **Stockage** : JSON pour les échanges, Pickle pour sauvegarder le modèle

## Installation

### Ce dont vous avez besoin

- Python 3.8 ou plus récent (si vous ne l'avez pas, téléchargez-le sur python.org)
- pip (normalement installé avec Python)

### Comment démarrer (3 étapes simples)

1. **Récupérez le code**
```bash
git clone <repository-url>
cd PFE_SMOFT_CRM_Intelligent
```

2. **Installez les bibliothèques nécessaires**
```bash
cd demo
pip install -r requirements.txt
```
(Ça va télécharger et installer tout ce qu'il faut - prenez un café, ça prend quelques minutes)

3. **Préparez le modèle** (seulement la première fois)
```bash
python scoring_model.py
```
(Le système va apprendre à partir des données d'exemple)

## Lancer le système

### La manière facile (recommandée)
Double-cliquez sur `start_server.bat` - c'est tout !

### Si vous préférez la ligne de commande
```bash
cd demo
python api.py
```

Une fois lancé, ouvrez votre navigateur et allez sur :
- **Pour tester** : http://localhost:8000/docs (interface interactive super pratique)
- **L'API elle-même** : http://localhost:8000
- **Documentation alternative** : http://localhost:8000/redoc (si vous préférez)

## Comment utiliser l'API

### Les fonctions principales

#### 1. Noter un seul client
```http
POST /api/score
Content-Type: application/json

{
  "customer_id": 1,
  "days_since_last_contact": 5,
  "total_contacts": 10,
  "total_spent": 1500.50,
  "emails_sent": 8,
  "emails_opened": 6,
  "website_visits": 15,
  "customer_age_days": 120
}
```

**Réponse :**
```json
{
  "customer_id": 1,
  "score": 85,
  "segment": "Hot",
  "recommendation": "Priorité HAUTE - Contacter immédiatement! Fort potentiel de conversion."
}
```

#### 2. Noter plusieurs clients en une fois
```http
POST /api/batch_score
Content-Type: application/json

{
  "clients": [
    {
      "customer_id": 1,
      "days_since_last_contact": 5,
      "total_contacts": 10,
      "total_spent": 1500.50,
      "emails_sent": 8,
      "emails_opened": 6,
      "website_visits": 15,
      "customer_age_days": 120
    }
  ]
}
```

#### 3. Voir comment le système fonctionne
```http
GET /api/stats
```

#### 4. Vérifier que tout fonctionne bien
```http
GET /health
```

## Les trois types de prospects

Voici comment le système classe vos clients :

| Segment | Score | Priorité | Action recommandée |
|---------|-------|----------|-------------------|
| **Hot** | ≥ 70 | HAUTE | Contacter immédiatement |
| **Warm** | 40-69 | MOYENNE | Suivi sous 48h |
| **Cold** | < 40 | BASSE | Relance automatique par email |

## Ce que le système regarde pour noter vos clients

Pour calculer le score, on analyse 7 éléments clés :

- **La fraîcheur de la relation** : Quand avez-vous parlé pour la dernière fois ?
- **La fréquence des échanges** : Combien de fois avez-vous été en contact ?
- **Le budget dépensé** : Combien le client a-t-il investi chez vous ?
- **L'intérêt par email** : Est-ce qu'il ouvre vos messages ?
- **Les visites sur votre site** : Est-ce qu'il vient voir ce que vous proposez ?
- **L'ancienneté** : Depuis combien de temps vous vous connaissez ?
- **Le score global RFM** : Une combinaison intelligente de tout ça

Plus ces indicateurs sont bons, plus le score est élevé !

## Tester que tout marche

Pour vérifier que l'API fonctionne correctement :
```bash
cd demo
python test_api.py
```
(Le script va faire quelques tests automatiques et vous dire si tout va bien)

## Comment l'utiliser dans votre code

### Si vous codez en Python
```python
from scoring_model import CRMScoringModel
import pandas as pd

# Charger le modèle
model = CRMScoringModel()
model.load_model('crm_scoring_model.pkl')

# Préparer les données
data = pd.DataFrame([{
    'customer_id': 1,
    'days_since_last_contact': 5,
    'total_contacts': 10,
    'total_spent': 1500.50,
    'emails_sent': 8,
    'emails_opened': 6,
    'website_visits': 15,
    'customer_age_days': 120
}])

# Scorer
features = model.create_features(data)
score = model.predict_score(features)[0]
segment = model.predict_segment([score])[0]

print(f"Score: {score}, Segment: {segment}")
```

### Si vous préférez passer par l'API (n'importe quel langage)
```python
import requests

response = requests.post('http://localhost:8000/api/score', json={
    "customer_id": 1,
    "days_since_last_contact": 5,
    "total_contacts": 10,
    "total_spent": 1500.50,
    "emails_sent": 8,
    "emails_opened": 6,
    "website_visits": 15,
    "customer_age_days": 120
})

result = response.json()
print(f"Score: {result['score']}, Segment: {result['segment']}")
```

## Personnalisation

### Sécurité (CORS)
Pour le moment, l'API accepte les connexions de n'importe où (pratique pour tester). 
Quand vous passerez en production, pensez à limiter ça dans `api.py` :
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-site.com"],  # Seulement votre site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Changer le port
Si le port 8000 est déjà utilisé sur votre machine, vous pouvez le changer dans `api.py` :
```python
uvicorn.run(app, host="0.0.0.0", port=VOTRE_PORT)  # Par exemple 8080
```

## Vous voulez améliorer le projet ?

Super ! Voici comment faire :

1. Faites un fork du projet (copiez-le dans votre compte)
2. Créez une branche pour votre amélioration (`git checkout -b ma-super-fonctionnalite`)
3. Faites vos modifications et enregistrez-les (`git commit -m 'Ajout de ma super fonctionnalité'`)
4. Envoyez vers votre fork (`git push origin ma-super-fonctionnalite`)
5. Proposez vos changements avec une Pull Request

On regardera avec plaisir !

## Auteurs

Samar Jelassi

## Changelog

### Version 1.0.0
- API REST complète avec FastAPI
- Modèle de scoring Random Forest
- Segmentation Hot/Warm/Cold
- Scoring individuel et batch
- Documentation Swagger automatique
- Tests API
