const API = "http://127.0.0.1:5050/api/etudiants";
let requestCount = 0;

// ============================================
// UTILITAIRES
// ============================================

function incrementRequests() {
    requestCount++;
    document.getElementById('totalRequetes').textContent = requestCount;
}

function showResult(elementId, content, isError = false) {
    const element = document.getElementById(elementId);
    element.style.display = 'block';
    element.className = isError ? 'result-box error' : 'result-box';
    element.textContent = content;
}

function showTab(tabName) {
    // Cacher tous les contenus
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // Désactiver tous les onglets
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Activer le bon contenu et onglet
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// ============================================
// VÉRIFICATION DU SERVEUR
// ============================================

async function verifierServeur() {
    try {
        const response = await fetch(API);
        if (response.ok) {
            document.getElementById('serverStatus').textContent = '✅ Serveur en ligne';
            document.getElementById('serverStatus').className = 'status';
            return true;
        }
    } catch (error) {
        document.getElementById('serverStatus').textContent = '❌ Serveur hors ligne';
        document.getElementById('serverStatus').className = 'status offline';
        return false;
    }
}

// ============================================
// GESTION DES ÉTUDIANTS
// ============================================

async function chargerEtudiants() {
    incrementRequests();

    try {
        const response = await fetch(API);
        const etudiants = await response.json();

        const liste = document.getElementById('listeEtudiants');
        liste.innerHTML = '';

        if (etudiants.length === 0) {
            liste.innerHTML = '<p style="color: #6b7280;">Aucun étudiant enregistré</p>';
            return;
        }

        // Mettre à jour les stats
        document.getElementById('totalEtudiants').textContent = etudiants.length;

        const filieres = [...new Set(etudiants.map(e => e.filiere))];
        document.getElementById('totalFilieres').textContent = filieres.length;

        etudiants.forEach(etudiant => {
            const div = document.createElement('div');
            div.className = 'list-item';
            div.innerHTML = `
                <div>
                    <strong>${etudiant.prenom} ${etudiant.nom}</strong>
                    <br>
                    <small style="color: #6b7280;">ID: ${etudiant.id} | ${etudiant.filiere}</small>
                </div>
                <div>
                    <button onclick="chargerPourModificationDirect(${etudiant.id})">✏️</button>
                    <button onclick="supprimerEtudiantDirect(${etudiant.id})" class="danger">🗑️</button>
                </div>
            `;
            liste.appendChild(div);
        });

    } catch (error) {
        showResult('listeEtudiants', 'Erreur: ' + error.message, true);
    }
}

async function ajouterEtudiant() {
    incrementRequests();

    const id = parseInt(document.getElementById('addId').value);
    const nom = document.getElementById('addNom').value;
    const prenom = document.getElementById('addPrenom').value;
    const filiere = document.getElementById('addFiliere').value;

    if (!id || !nom || !prenom || !filiere) {
        showResult('addResult', 'Erreur: Tous les champs sont requis', true);
        return;
    }

    try {
        const response = await fetch(API, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + btoa('admin:password123')
            },
            body: JSON.stringify({ id, nom, prenom, filiere })
        });

        const result = await response.json();

        if (response.ok) {
            showResult('addResult', '✅ ' + result.message);
            // Réinitialiser le formulaire
            document.getElementById('addId').value = '';
            document.getElementById('addNom').value = '';
            document.getElementById('addPrenom').value = '';
            document.getElementById('addFiliere').value = '';
            // Actualiser la liste
            chargerEtudiants();
        } else {
            showResult('addResult', '❌ ' + result.error, true);
        }
    } catch (error) {
        showResult('addResult', 'Erreur: ' + error.message, true);
    }
}

async function rechercherParId() {
    incrementRequests();

    const id = document.getElementById('searchId').value;

    if (!id) {
        showResult('searchResult', 'Erreur: Entrez un ID', true);
        return;
    }

    try {
        const response = await fetch(`${API}/${id}`);
        const result = await response.json();

        if (response.ok) {
            const formatted = `
✅ Étudiant trouvé:
═══════════════════════════════════
ID: ${result.id}
Nom: ${result.nom}
Prénom: ${result.prenom}
Filière: ${result.filiere}
═══════════════════════════════════`;
            showResult('searchResult', formatted);
        } else {
            showResult('searchResult', '❌ ' + result.error, true);
        }
    } catch (error) {
        showResult('searchResult', 'Erreur: ' + error.message, true);
    }
}

async function rechercherParFiliere() {
    incrementRequests();

    const filiere = document.getElementById('searchFiliere').value;

    if (!filiere) {
        showResult('searchResult', 'Erreur: Entrez une filière', true);
        return;
    }

    try {
        const response = await fetch(`${API}/filiere/${filiere}`);
        const etudiants = await response.json();

        if (etudiants.length === 0) {
            showResult('searchResult', `❌ Aucun étudiant trouvé dans la filière "${filiere}"`, true);
            return;
        }

        let result = `✅ ${etudiants.length} étudiant(s) trouvé(s) en ${filiere}:\n`;
        result += '═══════════════════════════════════\n';
        etudiants.forEach(e => {
            result += `ID ${e.id}: ${e.prenom} ${e.nom}\n`;
        });
        result += '═══════════════════════════════════';

        showResult('searchResult', result);
    } catch (error) {
        showResult('searchResult', 'Erreur: ' + error.message, true);
    }
}

async function chargerPourModification() {
    incrementRequests();

    const id = document.getElementById('modifyId').value;

    if (!id) {
        showResult('modifyResult', 'Erreur: Entrez un ID', true);
        return;
    }

    try {
        const response = await fetch(`${API}/${id}`);
        const etudiant = await response.json();

        if (response.ok) {
            document.getElementById('modifyNom').value = etudiant.nom;
            document.getElementById('modifyPrenom').value = etudiant.prenom;
            document.getElementById('modifyFiliere').value = etudiant.filiere;
            document.getElementById('modifyForm').style.display = 'block';
            showResult('modifyResult', '✅ Étudiant chargé - Modifiez les champs ci-dessous');
        } else {
            showResult('modifyResult', '❌ ' + etudiant.error, true);
        }
    } catch (error) {
        showResult('modifyResult', 'Erreur: ' + error.message, true);
    }
}

function chargerPourModificationDirect(id) {
    document.getElementById('modifyId').value = id;
    // Basculer vers l'onglet gestion
    showTab('gestion');
    // Scroller vers le formulaire de modification
    document.querySelector('#modifyId').scrollIntoView({ behavior: 'smooth' });
    // Charger les données
    setTimeout(() => chargerPourModification(), 500);
}

async function modifierEtudiant() {
    incrementRequests();

    const id = document.getElementById('modifyId').value;
    const nom = document.getElementById('modifyNom').value;
    const prenom = document.getElementById('modifyPrenom').value;
    const filiere = document.getElementById('modifyFiliere').value;

    if (!id || !nom || !prenom || !filiere) {
        showResult('modifyResult', 'Erreur: Tous les champs sont requis', true);
        return;
    }

    try {
        const response = await fetch(`${API}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + btoa('admin:password123')
            },
            body: JSON.stringify({ nom, prenom, filiere })
        });

        const result = await response.json();

        if (response.ok) {
            showResult('modifyResult', '✅ ' + result.message);
            chargerEtudiants();
        } else {
            showResult('modifyResult', '❌ ' + result.error, true);
        }
    } catch (error) {
        showResult('modifyResult', 'Erreur: ' + error.message, true);
    }
}

async function supprimerEtudiant() {
    incrementRequests();

    const id = document.getElementById('modifyId').value;

    if (!id) {
        showResult('modifyResult', 'Erreur: Entrez un ID', true);
        return;
    }

    if (!confirm(`Êtes-vous sûr de vouloir supprimer l'étudiant ID ${id} ?`)) {
        return;
    }

    try {
        const response = await fetch(`${API}/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': 'Basic ' + btoa('admin:password123')
            }
        });

        const result = await response.json();

        if (response.ok) {
            showResult('modifyResult', '✅ ' + result.message);
            document.getElementById('modifyForm').style.display = 'none';
            document.getElementById('modifyId').value = '';
            chargerEtudiants();
        } else {
            showResult('modifyResult', '❌ ' + result.error, true);
        }
    } catch (error) {
        showResult('modifyResult', 'Erreur: ' + error.message, true);
    }
}

async function supprimerEtudiantDirect(id) {
    if (!confirm(`Supprimer l'étudiant ID ${id} ?`)) {
        return;
    }

    incrementRequests();

    try {
        const response = await fetch(`${API}/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': 'Basic ' + btoa('admin:password123')
            }
        });

        const result = await response.json();

        if (response.ok) {
            alert('✅ ' + result.message);
            chargerEtudiants();
        } else {
            alert('❌ ' + result.error);
        }
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
}

function exporterJSON() {
    fetch(API)
        .then(res => res.json())
        .then(data => {
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'etudiants.json';
            a.click();
        });
}

// ============================================
// ATTAQUES DE SÉCURITÉ
// ============================================

async function attaqueBruteForce() {
    incrementRequests();

    const passwords = ['123456', 'password', 'admin', 'password123', '12345678', 'qwerty'];
    let result = '🔐 BRUTE FORCE - Tentative de deviner le mot de passe\n';
    result += '═══════════════════════════════════════════════════\n\n';

    showResult('bruteForceResult', result + '⏳ Test en cours...');

    for (let i = 0; i < passwords.length; i++) {
        const pwd = passwords[i];

        try {
            const response = await fetch(API, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + btoa(`admin:${pwd}`)
                },
                body: JSON.stringify({ id: 999, nom: 'Test', prenom: 'Test', filiere: 'Test' })
            });

            if (response.status === 201) {
                result += `✅ SUCCÈS! Mot de passe trouvé: ${pwd}\n`;
                result += `\n💡 Impact: Accès non autorisé au système\n`;
                result += `🛡️ Contremesure: Rate limiting, CAPTCHA, 2FA\n`;
                showResult('bruteForceResult', result);
                return;
            } else {
                result += `❌ Échec: ${pwd}\n`;
            }
        } catch (error) {
            result += `⚠️ Erreur: ${pwd}\n`;
        }

        showResult('bruteForceResult', result);
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    result += '\n❌ Aucun mot de passe trouvé dans la liste\n';
    showResult('bruteForceResult', result);
}

async function attaqueSQL() {
    incrementRequests();

    const payload = document.getElementById('sqlPayload').value;

    let result = '💉 INJECTION SQL\n';
    result += '═══════════════════════════════════════════════════\n\n';
    result += `Payload: ${payload}\n\n`;

    try {
        const response = await fetch('http://127.0.0.1:5050/api/debug/sql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: payload })
        });

        const data = await response.json();
        result += `Réponse du serveur:\n${JSON.stringify(data, null, 2)}\n\n`;
        result += `💡 Impact: Manipulation de la base de données\n`;
        result += `🛡️ Contremesure: Requêtes préparées, validation stricte\n`;

        showResult('sqlResult', result);
    } catch (error) {
        showResult('sqlResult', 'Erreur: ' + error.message, true);
    }
}

async function attaqueXSS() {
    incrementRequests();

    const payload = document.getElementById('xssPayload').value;

    let result = '💥 CROSS-SITE SCRIPTING (XSS)\n';
    result += '═══════════════════════════════════════════════════\n\n';
    result += `Payload: ${payload}\n\n`;

    try {
        const response = await fetch('http://127.0.0.1:5050/api/debug/xss', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: payload })
        });

        const data = await response.json();
        result += `Réponse du serveur:\n${JSON.stringify(data, null, 2)}\n\n`;

        // DANGER: Injection directe pour démonstration
        document.getElementById('xssZone').innerHTML = data.html;

        result += `⚠️ Le code a été injecté dans la zone ci-dessous!\n`;
        result += `💡 Impact: Vol de session, phishing, malware\n`;
        result += `🛡️ Contremesure: Échappement HTML, CSP\n`;

        showResult('xssResult', result);
    } catch (error) {
        showResult('xssResult', 'Erreur: ' + error.message, true);
    }
}

async function attaqueDoS() {
    incrementRequests();

    const count = parseInt(document.getElementById('dosCount').value) || 50;

    let result = '⚡ DÉNI DE SERVICE (DoS)\n';
    result += '═══════════════════════════════════════════════════\n\n';
    result += `Envoi de ${count} requêtes rapides...\n\n`;

    showResult('dosResult', result + '⏳ Attaque en cours...');

    const startTime = Date.now();
    let success = 0;
    let failed = 0;

    const promises = [];
    for (let i = 0; i < count; i++) {
        promises.push(
            fetch(API)
                .then(() => success++)
                .catch(() => failed++)
        );
    }

    await Promise.all(promises);

    const duration = ((Date.now() - startTime) / 1000).toFixed(2);

    result += `✅ Requêtes réussies: ${success}\n`;
    result += `❌ Requêtes échouées: ${failed}\n`;
    result += `⏱️ Durée totale: ${duration} secondes\n`;
    result += `📊 Débit: ${(count / duration).toFixed(2)} req/s\n\n`;
    result += `💡 Impact: Surcharge serveur, indisponibilité\n`;
    result += `🛡️ Contremesure: Rate limiting, CDN, CAPTCHA\n`;

    showResult('dosResult', result);
}

async function attaqueIDOR() {
    incrementRequests();

    const range = document.getElementById('idorRange').value;
    const [start, end] = range.split('-').map(Number);

    if (!start || !end) {
        showResult('idorResult', 'Erreur: Format invalide. Utilisez: 1-10', true);
        return;
    }

    let result = '🔓 IDOR - Insecure Direct Object Reference\n';
    result += '═══════════════════════════════════════════════════\n\n';
    result += `Énumération des IDs de ${start} à ${end}...\n\n`;

    showResult('idorResult', result + '⏳ Scan en cours...');

    for (let id = start; id <= end; id++) {
        try {
            const response = await fetch(`${API}/${id}`);

            if (response.ok) {
                const etudiant = await response.json();
                result += `✅ ID ${id}: ${etudiant.prenom} ${etudiant.nom} (${etudiant.filiere})\n`;
            } else {
                result += `❌ ID ${id}: Non trouvé\n`;
            }
        } catch (error) {
            result += `⚠️ ID ${id}: Erreur\n`;
        }

        showResult('idorResult', result);
        await new Promise(resolve => setTimeout(resolve, 200));
    }

    result += `\n💡 Impact: Accès à des données non autorisées\n`;
    result += `🛡️ Contremesure: UUIDs, vérification des permissions\n`;

    showResult('idorResult', result);
}

function verifierHTTPS() {
    let result = '🔒 VÉRIFICATION HTTPS\n';
    result += '═══════════════════════════════════════════════════\n\n';

    const protocol = window.location.protocol;
    const apiProtocol = new URL(API).protocol;

    result += `Protocol de la page: ${protocol}\n`;
    result += `Protocol de l'API: ${apiProtocol}\n\n`;

    if (protocol === 'http:' || apiProtocol === 'http:') {
        result += `❌ VULNÉRABLE: Communication non chiffrée\n\n`;
        result += `Les données sont transmises en CLAIR:\n`;
        result += `- Identifiants de connexion\n`;
        result += `- Données personnelles\n`;
        result += `- Cookies de session\n\n`;
        result += `💡 Impact: Interception (Man-in-the-Middle)\n`;
        result += `🛡️ Contremesure: HTTPS obligatoire, HSTS\n`;
    } else {
        result += `✅ SÉCURISÉ: Communication chiffrée\n`;
    }

    showResult('httpsResult', result);
}

// ============================================
// AUTRES FONCTIONS
// ============================================

function ouvrirAPI() {
    window.open('http://127.0.0.1:5050/', '_blank');
}

// ============================================
// INITIALISATION
// ============================================

window.addEventListener('load', () => {
    verifierServeur();
    chargerEtudiants();

    // Vérifier le serveur toutes les 30 secondes
    setInterval(verifierServeur, 30000);
});