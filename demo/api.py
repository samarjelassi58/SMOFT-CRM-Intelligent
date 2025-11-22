"""
API REST pour le CRM Intelligent SMOFT
Expose les fonctionnalités de scoring via FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
from scoring_model import CRMScoringModel
import uvicorn

# Initialisation de l'API
app = FastAPI(
    title="SMOFT CRM Intelligent API",
    description="API de scoring et relance automatisée pour CRM SMOFT",
    version="1.0.0"
)

# Configuration CORS pour autoriser les requêtes depuis l'interface web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines (pour le développement)
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP
    allow_headers=["*"],  # Permet tous les headers
)

# Chargement du modèle pré-entraîné
scoring_model = CRMScoringModel()

# Models Pydantic pour validation des données
class ClientData(BaseModel):
    """Données d'un client CRM"""
    customer_id: int
    days_since_last_contact: int
    total_contacts: int
    total_spent: float
    emails_sent: int
    emails_opened: int
    website_visits: int
    customer_age_days: int

class ScoringResponse(BaseModel):
    """Réponse du scoring"""
    customer_id: int
    score: int
    segment: str
    recommendation: str

class BatchScoringRequest(BaseModel):
    """Demande de scoring en batch"""
    clients: List[ClientData]


# Routes API

@app.get("/")
def root():
    """Page d'accueil de l'API"""
    return {
        "message": "SMOFT CRM Intelligent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "score": "/api/score",
            "batch_score": "/api/batch_score",
            "stats": "/api/stats"
        }
    }

@app.get("/health")
def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "model_loaded": scoring_model.is_trained
    }

@app.post("/api/score", response_model=ScoringResponse)
def score_client(client: ClientData):
    """
    Scorer un client individuel
    
    Args:
        client: Données du client CRM
        
    Returns:
        Score de conversion, segment et recommandation
    """
    if not scoring_model.is_trained:
        raise HTTPException(
            status_code=503, 
            detail="Le modèle n'est pas chargé. Veuillez entraîner le modèle d'abord."
        )
    
    try:
        # Conversion en DataFrame
        df = pd.DataFrame([client.dict()])
        
        # Feature engineering
        features = scoring_model.create_features(df)
        
        # Prédiction
        score = scoring_model.predict_score(features)[0]
        segment = scoring_model.predict_segment([score])[0]
        
        # Recommandation basée sur le segment
        recommendations = {
            'Hot': "🔥 Priorité HAUTE - Contacter immédiatement! Fort potentiel de conversion.",
            'Warm': "⚡ Priorité MOYENNE - Planifier un suivi sous 48h. Prospect intéressé.",
            'Cold': "❄️ Priorité BASSE - Relance automatique par email. Nourrir le lead."
        }
        
        return ScoringResponse(
            customer_id=client.customer_id,
            score=score,
            segment=segment,
            recommendation=recommendations[segment]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du scoring: {str(e)}")

@app.post("/api/batch_score")
def batch_score_clients(request: BatchScoringRequest):
    """
    Scorer plusieurs clients en batch
    
    Args:
        request: Liste de clients à scorer
        
    Returns:
        Liste des scores et segments
    """
    if not scoring_model.is_trained:
        raise HTTPException(
            status_code=503,
            detail="Le modèle n'est pas chargé."
        )
    
    try:
        # Conversion en DataFrame
        clients_data = [client.dict() for client in request.clients]
        df = pd.DataFrame(clients_data)
        
        # Feature engineering
        features = scoring_model.create_features(df)
        
        # Prédictions
        scores = scoring_model.predict_score(features)
        segments = scoring_model.predict_segment(scores)
        
        # Construction de la réponse
        results = []
        for i, client in enumerate(request.clients):
            results.append({
                "customer_id": client.customer_id,
                "score": int(scores[i]),
                "segment": segments[i]
            })
        
        # Statistiques du batch
        stats = {
            "total_clients": len(results),
            "hot_leads": sum(1 for r in results if r['segment'] == 'Hot'),
            "warm_leads": sum(1 for r in results if r['segment'] == 'Warm'),
            "cold_leads": sum(1 for r in results if r['segment'] == 'Cold'),
            "average_score": sum(r['score'] for r in results) / len(results)
        }
        
        return {
            "results": results,
            "statistics": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du batch scoring: {str(e)}")

@app.get("/api/stats")
def get_model_stats():
    """
    Récupérer les statistiques du modèle
    """
    if not scoring_model.is_trained:
        raise HTTPException(status_code=503, detail="Modèle non entraîné")
    
    feature_importance = scoring_model.get_feature_importance()
    feature_names = [
        'recency_days', 'contact_frequency', 'total_purchase_amount',
        'email_open_rate', 'website_visits', 'customer_age_days', 'rfm_score'
    ]
    
    return {
        "model_type": "RandomForestClassifier",
        "n_estimators": 100,
        "feature_importance": {
            name: float(importance) 
            for name, importance in zip(feature_names, feature_importance)
        },
        "segments": {
            "Hot": "Score >= 70",
            "Warm": "40 <= Score < 70",
            "Cold": "Score < 40"
        }
    }

@app.post("/api/load_model")
def load_model(model_path: str = "crm_scoring_model.pkl"):
    """
    Charger un modèle pré-entraîné
    """
    try:
        scoring_model.load_model(model_path)
        return {
            "message": "Modèle chargé avec succès",
            "model_path": model_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de chargement: {str(e)}")


# Script de démarrage
if __name__ == "__main__":
    print("🚀 Démarrage de l'API CRM Intelligent SMOFT...")
    print("📡 API disponible sur: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    
    # Charger automatiquement le modèle au démarrage
    import os
    model_path = "crm_scoring_model.pkl"
    if os.path.exists(model_path):
        try:
            scoring_model.load_model(model_path)
            print("✅ Modèle chargé automatiquement")
        except Exception as e:
            print(f"⚠️ Erreur de chargement du modèle: {e}")
    else:
        print("⚠️ Modèle non trouvé. Veuillez exécuter scoring_model.py d'abord.")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
