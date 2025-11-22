"""
Script de test de l'API CRM Intelligent
Démontre l'utilisation de l'API REST
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test du endpoint health"""
    print("🔍 Test du health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()

def test_single_score():
    """Test du scoring d'un client unique"""
    print("🎯 Test du scoring individuel...")
    
    client_data = {
        "customer_id": 12345,
        "days_since_last_contact": 15,
        "total_contacts": 25,
        "total_spent": 5000.0,
        "emails_sent": 50,
        "emails_opened": 35,
        "website_visits": 120,
        "customer_age_days": 365
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/score",
        json=client_data
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Client ID: {result['customer_id']}")
        print(f"   Score: {result['score']}/100")
        print(f"   Segment: {result['segment']}")
        print(f"   Recommandation: {result['recommendation']}")
    else:
        print(f"   Erreur: {response.text}")
    print()

def test_batch_score():
    """Test du scoring en batch"""
    print("📊 Test du batch scoring...")
    
    clients = [
        {
            "customer_id": 1001,
            "days_since_last_contact": 5,
            "total_contacts": 30,
            "total_spent": 8000.0,
            "emails_sent": 60,
            "emails_opened": 45,
            "website_visits": 150,
            "customer_age_days": 500
        },
        {
            "customer_id": 1002,
            "days_since_last_contact": 90,
            "total_contacts": 5,
            "total_spent": 500.0,
            "emails_sent": 20,
            "emails_opened": 3,
            "website_visits": 10,
            "customer_age_days": 60
        },
        {
            "customer_id": 1003,
            "days_since_last_contact": 30,
            "total_contacts": 15,
            "total_spent": 3000.0,
            "emails_sent": 40,
            "emails_opened": 20,
            "website_visits": 50,
            "customer_age_days": 200
        }
    ]
    
    response = requests.post(
        f"{API_BASE_URL}/api/batch_score",
        json={"clients": clients}
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"\n   📈 Statistiques du batch:")
        stats = result['statistics']
        print(f"      • Total clients: {stats['total_clients']}")
        print(f"      • Hot leads: {stats['hot_leads']}")
        print(f"      • Warm leads: {stats['warm_leads']}")
        print(f"      • Cold leads: {stats['cold_leads']}")
        print(f"      • Score moyen: {stats['average_score']:.1f}/100")
        
        print(f"\n   📋 Résultats détaillés:")
        for r in result['results']:
            print(f"      • Client #{r['customer_id']}: Score {r['score']}/100 - Segment {r['segment']}")
    else:
        print(f"   Erreur: {response.text}")
    print()

def test_model_stats():
    """Test du endpoint de statistiques"""
    print("📊 Test des statistiques du modèle...")
    
    response = requests.get(f"{API_BASE_URL}/api/stats")
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   Type de modèle: {stats['model_type']}")
        print(f"\n   🔍 Feature Importance:")
        for feature, importance in sorted(
            stats['feature_importance'].items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            print(f"      • {feature:25s}: {importance:.3f}")
    else:
        print(f"   Erreur: {response.text}")
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTS DE L'API CRM INTELLIGENT SMOFT")
    print("=" * 70)
    print()
    
    print("⚠️  Assurez-vous que l'API est démarrée (python api.py)")
    print()
    
    try:
        test_health()
        # Tests complets du scoring
        test_single_score()
        test_batch_score()
        test_model_stats()
        
        print("✅ Tests terminés!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("   Vérifiez que l'API est démarrée sur http://localhost:8000")
