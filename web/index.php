<?php
/**
 * CRM Intelligent SMOFT - Interface Web
 * Tableau de bord de scoring et relance automatisée
 */

// Configuration de l'API
define('API_BASE_URL', 'http://localhost:8000');

// Fonction pour appeler l'API
function callAPI($endpoint, $method = 'GET', $data = null) {
    $url = API_BASE_URL . $endpoint;
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    }
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        return json_decode($response, true);
    }
    return null;
}

// Vérifier l'état de l'API
$apiHealth = callAPI('/health');
$apiStatus = $apiHealth ? 'connected' : 'disconnected';
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRM Intelligent SMOFT - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }

        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            color: #666;
            font-size: 1.1em;
        }

        .api-status {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 15px;
        }

        .api-status.connected {
            background: #d4edda;
            color: #155724;
        }

        .api-status.disconnected {
            background: #f8d7da;
            color: #721c24;
        }

        .api-status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .connected .api-status-dot {
            background: #28a745;
        }

        .disconnected .api-status-dot {
            background: #dc3545;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        }

        .card-title {
            font-size: 1.3em;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-icon {
            font-size: 1.5em;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }

        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn:active {
            transform: translateY(0);
        }

        .result {
            display: none;
            margin-top: 25px;
            padding: 20px;
            border-radius: 10px;
            animation: slideIn 0.5s;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .result.hot {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
        }

        .result.warm {
            background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
            color: #333;
        }

        .result.cold {
            background: linear-gradient(135deg, #54a0ff 0%, #00d2d3 100%);
            color: white;
        }

        .result h3 {
            font-size: 1.5em;
            margin-bottom: 15px;
        }

        .score-display {
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
        }

        .recommendation {
            font-size: 1.1em;
            line-height: 1.6;
            margin-top: 15px;
            padding: 15px;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }

        .loader {
            display: none;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .info-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-top: 30px;
        }

        .info-section h2 {
            color: #667eea;
            margin-bottom: 20px;
        }

        .info-section p {
            color: #666;
            line-height: 1.8;
            margin-bottom: 15px;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .feature {
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }

        .feature h3 {
            color: #333;
            margin-bottom: 10px;
        }

        .feature p {
            color: #666;
            font-size: 0.95em;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🎯 CRM Intelligent SMOFT</h1>
            <p>Agent IA de Scoring & Relance Automatisée</p>
            <div class="api-status <?php echo $apiStatus; ?>">
                <span class="api-status-dot"></span>
                <?php if ($apiStatus === 'connected'): ?>
                    API Connectée - Modèle <?php echo $apiHealth['model_loaded'] ? 'Chargé ✅' : 'Non Chargé ⚠️'; ?>
                <?php else: ?>
                    API Déconnectée - Veuillez démarrer l'API Python
                <?php endif; ?>
            </div>
        </div>

        <?php if ($apiStatus === 'connected'): ?>
        <!-- Dashboard -->
        <div class="dashboard">
            <!-- Formulaire de Scoring -->
            <div class="card">
                <div class="card-title">
                    <span class="card-icon">📊</span>
                    Scorer un Client
                </div>
                <form id="scoringForm">
                    <div class="form-group">
                        <label>ID Client</label>
                        <input type="number" name="customer_id" value="12345" required>
                    </div>
                    <div class="form-group">
                        <label>Jours depuis dernier contact</label>
                        <input type="number" name="days_since_last_contact" value="15" required>
                    </div>
                    <div class="form-group">
                        <label>Nombre total de contacts</label>
                        <input type="number" name="total_contacts" value="25" required>
                    </div>
                    <div class="form-group">
                        <label>Montant total dépensé (€)</label>
                        <input type="number" step="0.01" name="total_spent" value="5000" required>
                    </div>
                    <div class="form-group">
                        <label>Emails envoyés</label>
                        <input type="number" name="emails_sent" value="50" required>
                    </div>
                    <div class="form-group">
                        <label>Emails ouverts</label>
                        <input type="number" name="emails_opened" value="35" required>
                    </div>
                    <div class="form-group">
                        <label>Visites du site web</label>
                        <input type="number" name="website_visits" value="120" required>
                    </div>
                    <div class="form-group">
                        <label>Ancienneté client (jours)</label>
                        <input type="number" name="customer_age_days" value="365" required>
                    </div>
                    <button type="submit" class="btn">🎯 Calculer le Score</button>
                </form>
                <div class="loader" id="loader"></div>
                <div id="result" class="result"></div>
            </div>

            <!-- Statistiques du Modèle -->
            <div class="card">
                <div class="card-title">
                    <span class="card-icon">📈</span>
                    Statistiques du Modèle
                </div>
                <div id="modelStats">
                    <p style="color: #999; text-align: center;">Chargement des statistiques...</p>
                </div>
            </div>
        </div>

        <!-- Section d'Information -->
        <div class="info-section">
            <h2>🚀 Comment ça fonctionne ?</h2>
            <p>
                Le CRM Intelligent SMOFT utilise l'intelligence artificielle pour évaluer automatiquement 
                le potentiel de conversion de chaque client ou prospect. Le système analyse plusieurs 
                facteurs comportementaux et transactionnels pour attribuer un score de 0 à 100.
            </p>

            <div class="features">
                <div class="feature">
                    <h3>🔥 Hot Leads (Score ≥ 70)</h3>
                    <p>Priorité HAUTE - Ces prospects ont un fort potentiel de conversion. Contactez-les immédiatement!</p>
                </div>
                <div class="feature">
                    <h3>⚡ Warm Leads (Score 40-69)</h3>
                    <p>Priorité MOYENNE - Prospects intéressés nécessitant un suivi sous 48h pour maintenir l'engagement.</p>
                </div>
                <div class="feature">
                    <h3>❄️ Cold Leads (Score < 40)</h3>
                    <p>Priorité BASSE - Automatisez les relances par email pour nourrir progressivement ces leads.</p>
                </div>
            </div>
        </div>

        <?php else: ?>
        <!-- Message d'erreur API -->
        <div class="info-section" style="background: #f8d7da; border-left: 5px solid #dc3545;">
            <h2 style="color: #721c24;">⚠️ API Non Disponible</h2>
            <p style="color: #721c24;">
                L'API Python n'est pas accessible. Veuillez suivre ces étapes :
            </p>
            <ol style="color: #721c24; margin-left: 30px; line-height: 2;">
                <li>Ouvrez un terminal dans le dossier du projet</li>
                <li>Activez l'environnement virtuel : <code>.venv\Scripts\activate</code></li>
                <li>Démarrez l'API : <code>python demo/api.py</code></li>
                <li>Rechargez cette page</li>
            </ol>
        </div>
        <?php endif; ?>
    </div>

    <script>
        // Formulaire de scoring
        document.getElementById('scoringForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = key === 'customer_id' || key === 'days_since_last_contact' || 
                            key === 'total_contacts' || key === 'emails_sent' || 
                            key === 'emails_opened' || key === 'website_visits' || 
                            key === 'customer_age_days' 
                            ? parseInt(value) 
                            : parseFloat(value);
            });

            const loader = document.getElementById('loader');
            const result = document.getElementById('result');
            
            loader.style.display = 'block';
            result.style.display = 'none';

            try {
                const response = await fetch('<?php echo API_BASE_URL; ?>/api/score', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                const scoreData = await response.json();
                
                loader.style.display = 'none';
                result.style.display = 'block';
                result.className = 'result ' + scoreData.segment.toLowerCase();
                
                let segmentIcon = '';
                if (scoreData.segment === 'Hot') segmentIcon = '🔥';
                else if (scoreData.segment === 'Warm') segmentIcon = '⚡';
                else segmentIcon = '❄️';

                result.innerHTML = `
                    <h3>${segmentIcon} Segment: ${scoreData.segment}</h3>
                    <div class="score-display">${scoreData.score}/100</div>
                    <div class="recommendation">
                        <strong>Recommandation:</strong><br>
                        ${scoreData.recommendation}
                    </div>
                `;
            } catch (error) {
                loader.style.display = 'none';
                result.style.display = 'block';
                result.className = 'result';
                result.style.background = '#f8d7da';
                result.style.color = '#721c24';
                result.innerHTML = '<h3>❌ Erreur</h3><p>Impossible de calculer le score. Vérifiez l\'API.</p>';
            }
        });

        // Charger les statistiques du modèle
        async function loadModelStats() {
            try {
                const response = await fetch('<?php echo API_BASE_URL; ?>/api/stats');
                const stats = await response.json();
                
                // Trier les features par importance
                const sortedFeatures = Object.entries(stats.feature_importance)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 5);

                let html = `
                    <div class="stat-item" style="grid-column: 1 / -1;">
                        <div class="stat-value">${stats.model_type}</div>
                        <div class="stat-label">Type de Modèle</div>
                    </div>
                    <div style="grid-column: 1 / -1; margin-top: 20px;">
                        <h4 style="margin-bottom: 15px; color: #333;">Top Features</h4>
                `;

                sortedFeatures.forEach(([feature, importance]) => {
                    const percentage = (importance * 100).toFixed(1);
                    html += `
                        <div style="margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span style="color: #666;">${feature}</span>
                                <span style="color: #667eea; font-weight: bold;">${percentage}%</span>
                            </div>
                            <div style="background: #e0e0e0; height: 8px; border-radius: 4px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: ${percentage}%; transition: width 0.5s;"></div>
                            </div>
                        </div>
                    `;
                });

                html += '</div>';
                document.getElementById('modelStats').innerHTML = html;
            } catch (error) {
                document.getElementById('modelStats').innerHTML = 
                    '<p style="color: #dc3545; text-align: center;">Erreur de chargement des statistiques</p>';
            }
        }

        // Charger les stats au chargement de la page
        if (document.getElementById('modelStats')) {
            loadModelStats();
        }
    </script>
</body>
</html>
