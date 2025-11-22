"""
CRM Intelligent - Modèle de Scoring Client
Agent IA pour prédire le potentiel de conversion des prospects
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
from datetime import datetime, timedelta

class CRMScoringModel:
    """
    Modèle de scoring intelligent pour CRM SMOFT
    Prédit la probabilité de conversion d'un prospect/client
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.is_trained = False
        
    def create_features(self, df):
        """
        Feature Engineering - Extraction des caractéristiques pertinentes
        
        Features calculées:
        - RFM (Recency, Frequency, Monetary)
        - Engagement score
        - Comportemental features
        """
        features = pd.DataFrame()
        
        # Recency: Jours depuis dernière interaction
        features['recency_days'] = df['days_since_last_contact']
        
        # Frequency: Nombre d'interactions
        features['contact_frequency'] = df['total_contacts']
        
        # Monetary: Montant total des achats
        features['total_purchase_amount'] = df['total_spent']
        
        # Engagement: Taux d'ouverture des emails
        features['email_open_rate'] = df['emails_opened'] / (df['emails_sent'] + 1)
        
        # Behavioral: Visites du site
        features['website_visits'] = df['website_visits']
        
        # Temps en tant que client (jours)
        features['customer_age_days'] = df['customer_age_days']
        
        # Score composite RFM
        features['rfm_score'] = (
            (100 - features['recency_days']) * 0.3 +
            features['contact_frequency'] * 0.3 +
            (features['total_purchase_amount'] / 100) * 0.4
        )
        
        return features
    
    def train(self, X_train, y_train):
        """
        Entraînement du modèle de scoring
        """
        print("🚀 Entraînement du modèle de scoring CRM...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("✅ Modèle entraîné avec succès!")
        
    def predict_score(self, X):
        """
        Prédire le score de conversion (0-100)
        """
        if not self.is_trained:
            raise Exception("Le modèle n'est pas encore entraîné!")
        
        # Probabilité de conversion
        proba = self.model.predict_proba(X)[:, 1]
        
        # Conversion en score 0-100
        scores = (proba * 100).astype(int)
        
        return scores
    
    def predict_segment(self, scores):
        """
        Segmentation automatique basée sur le score
        - Hot (Chaud): score >= 70
        - Warm (Tiède): 40 <= score < 70
        - Cold (Froid): score < 40
        """
        segments = []
        for score in scores:
            if score >= 70:
                segments.append('Hot')
            elif score >= 40:
                segments.append('Warm')
            else:
                segments.append('Cold')
        return segments
    
    def get_feature_importance(self):
        """
        Retourne l'importance de chaque feature
        Utile pour comprendre quels facteurs influencent le scoring
        """
        if not self.is_trained:
            raise Exception("Le modèle n'est pas encore entraîné!")
        
        return self.model.feature_importances_
    
    def save_model(self, filepath='crm_scoring_model.pkl'):
        """
        Sauvegarder le modèle entraîné
        """
        joblib.dump(self.model, filepath)
        print(f"✅ Modèle sauvegardé: {filepath}")
    
    def load_model(self, filepath='crm_scoring_model.pkl'):
        """
        Charger un modèle pré-entraîné
        """
        self.model = joblib.load(filepath)
        self.is_trained = True
        print(f"✅ Modèle chargé: {filepath}")


def generate_sample_data(n_samples=1000):
    """
    Génère des données CRM synthétiques pour la démonstration
    """
    np.random.seed(42)
    
    data = {
        'customer_id': range(1, n_samples + 1),
        'days_since_last_contact': np.random.randint(1, 365, n_samples),
        'total_contacts': np.random.randint(1, 50, n_samples),
        'total_spent': np.random.uniform(0, 10000, n_samples),
        'emails_sent': np.random.randint(5, 100, n_samples),
        'emails_opened': np.random.randint(0, 80, n_samples),
        'website_visits': np.random.randint(0, 200, n_samples),
        'customer_age_days': np.random.randint(30, 1825, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Générer la variable cible (conversion) avec une logique réaliste
    conversion_proba = (
        (365 - df['days_since_last_contact']) / 365 * 0.3 +
        np.minimum(df['total_contacts'] / 50, 1) * 0.25 +
        np.minimum(df['total_spent'] / 10000, 1) * 0.25 +
        (df['emails_opened'] / df['emails_sent']) * 0.2
    )
    
    df['converted'] = (np.random.random(n_samples) < conversion_proba).astype(int)
    
    return df


def demo_scoring_workflow():
    """
    Démonstration complète du workflow de scoring
    """
    print("=" * 70)
    print("🎯 DÉMONSTRATION - CRM INTELLIGENT SMOFT")
    print("Agent IA de Scoring & Relance Automatisée")
    print("=" * 70)
    print()
    
    # 1. Génération de données de test
    print("📊 Génération de données CRM de test...")
    df = generate_sample_data(n_samples=1000)
    print(f"✅ {len(df)} clients générés")
    print()
    
    # 2. Préparation des données
    print("🔧 Feature Engineering...")
    model = CRMScoringModel()
    X = model.create_features(df)
    y = df['converted']
    print(f"✅ {X.shape[1]} features créées")
    print(f"   Features: {list(X.columns)}")
    print()
    
    # 3. Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 4. Entraînement
    model.train(X_train, y_train)
    print()
    
    # 5. Prédictions
    print("🎯 Prédiction des scores...")
    scores_test = model.predict_score(X_test)
    segments_test = model.predict_segment(scores_test)
    
    # 6. Évaluation
    y_pred = (scores_test >= 50).astype(int)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Précision du modèle: {accuracy:.2%}")
    print()
    
    # 7. Analyse des segments
    print("📈 Distribution des segments:")
    unique, counts = np.unique(segments_test, return_counts=True)
    for seg, count in zip(unique, counts):
        percentage = count / len(segments_test) * 100
        print(f"   • {seg:6s}: {count:3d} clients ({percentage:5.1f}%)")
    print()
    
    # 8. Feature Importance
    print("🔍 Importance des features:")
    feature_importance = model.get_feature_importance()
    feature_names = X.columns
    
    for name, importance in sorted(zip(feature_names, feature_importance), 
                                   key=lambda x: x[1], reverse=True):
        print(f"   • {name:25s}: {importance:.3f}")
    print()
    
    # 9. Exemples de scoring
    print("💼 Exemples de clients scorés:")
    print("-" * 70)
    sample_indices = np.random.choice(len(X_test), 5, replace=False)
    
    for idx in sample_indices:
        score = scores_test[idx]
        segment = segments_test[idx]
        actual = "✅ Converti" if y_test.iloc[idx] == 1 else "❌ Non converti"
        
        print(f"   Client #{idx + 1}:")
        print(f"     Score: {score}/100 | Segment: {segment:6s} | Réalité: {actual}")
    
    print("=" * 70)
    print()
    
    # 10. Sauvegarde du modèle
    model.save_model('crm_scoring_model.pkl')
    
    return model, X_test, y_test, scores_test


if __name__ == "__main__":
    # Lancer la démonstration
    model, X_test, y_test, scores = demo_scoring_workflow()
    
    print("🎉 Démonstration terminée!")
    print("📦 Fichiers générés:")
    print("   • crm_scoring_model.pkl (modèle entraîné)")
    print()
    print("🚀 Prochaines étapes:")
    print("   1. Intégrer avec l'API REST (voir api.py)")
    print("   2. Connecter à la base de données CRM SMOFT")
    print("   3. Automatiser les relances basées sur les segments")
