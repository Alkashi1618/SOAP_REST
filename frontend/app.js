const API = "http://127.0.0.1:5050/api/etudiants";
let requestCount = 0;

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
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

async function verifierServeur() {
    try {
        const response = await fetch(API);
        if (response.ok) {
            document.getElementById('serverStatus').textContent = 'Server Online';
            document.getElementById('serverStatus').className = 'status';
            return true;
        }
    } catch (error) {
        document.getElementById('serverStatus').textContent = 'Server Offline';
        document.getElementById('serverStatus').className = 'status offline';
        return false;
    }
}

async function chargerEtudiants() {
    incrementRequests();

    try {
        const response = await fetch(API);
        const etudiants = await response.json();

        const liste = document.getElementById('listeEtudiants');
        liste.innerHTML = '';

        if (etudiants.length === 0) {
            liste.innerHTML = '<p style="color: #64748b;">No students registered</p>';
            return;
        }

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
                    <small>ID: ${etudiant.id} | ${etudiant.filiere}</small>
                </div>
                <div>
                    <button onclick="chargerPourModificationDirect(${etudiant.id})">Edit</button>
                    <button onclick="supprimerEtudiantDirect(${etudiant.id})" class="danger">Delete</button>
                </div>
            `;
            liste.appendChild(div);
        });

    } catch (error) {
        showResult('listeEtudiants', 'Error: ' + error.message, true);
    }
}

async function ajouterEtudiant() {
    incrementRequests();

    const id = parseInt(document.getElementById('addId').value);
    const nom = document.getElementById('addNom').value;
    const prenom = document.getElementById('addPrenom').value;
    const filiere = document.getElementById('addFiliere').value;

    if (!id || !nom || !prenom || !filiere) {
        showResult('addResult', 'Error: All fields are required', true);
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
            showResult('addResult', 'SUCCESS: ' + result.message);
            document.getElementById('addId').value = '';
            document.getElementById('addNom').value = '';
            document.getElementById('addPrenom').value = '';
            document.getElementById('addFiliere').value = '';
            chargerEtudiants();
        } else {
            showResult('addResult', 'ERROR: ' + result.error, true);
        }
    } catch (error) {
        showResult('addResult', 'Error: ' + error.message, true);
    }
}

async function rechercherParId() {
    incrementRequests();

    const id = document.getElementById('searchId').value;

    if (!id) {
        showResult('searchResult', 'Error: Enter an ID', true);
        return;
    }

    try {
        const response = await fetch(`${API}/${id}`);
        const result = await response.json();

        if (response.ok) {
            const formatted = `Student Found:\nID: ${result.id}\nLast Name: ${result.nom}\nFirst Name: ${result.prenom}\nDepartment: ${result.filiere}`;
            showResult('searchResult', formatted);
        } else {
            showResult('searchResult', 'ERROR: ' + result.error, true);
        }
    } catch (error) {
        showResult('searchResult', 'Error: ' + error.message, true);
    }
}

async function rechercherParFiliere() {
    incrementRequests();

    const filiere = document.getElementById('searchFiliere').value;

    if (!filiere) {
        showResult('searchResult', 'Error: Enter a department', true);
        return;
    }

    try {
        const response = await fetch(`${API}/filiere/${filiere}`);
        const etudiants = await response.json();

        if (etudiants.length === 0) {
            showResult('searchResult', `No students found in department: ${filiere}`, true);
            return;
        }

        let result = `${etudiants.length} student(s) found in ${filiere}:\n\n`;
        etudiants.forEach(e => {
            result += `ID ${e.id}: ${e.prenom} ${e.nom}\n`;
        });

        showResult('searchResult', result);
    } catch (error) {
        showResult('searchResult', 'Error: ' + error.message, true);
    }
}

async function chargerPourModification() {
    incrementRequests();

    const id = document.getElementById('modifyId').value;

    if (!id) {
        showResult('modifyResult', 'Error: Enter an ID', true);
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
            showResult('modifyResult', 'Student loaded - Modify fields below');
        } else {
            showResult('modifyResult', 'ERROR: ' + etudiant.error, true);
        }
    } catch (error) {
        showResult('modifyResult', 'Error: ' + error.message, true);
    }
}

function chargerPourModificationDirect(id) {
    document.getElementById('modifyId').value = id;
    showTab('management');
    document.querySelector('#modifyId').scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => chargerPourModification(), 500);
}

async function modifierEtudiant() {
    incrementRequests();

    const id = document.getElementById('modifyId').value;
    const nom = document.getElementById('modifyNom').value;
    const prenom = document.getElementById('modifyPrenom').value;
    const filiere = document.getElementById('modifyFiliere').value;

    if (!id || !nom || !prenom || !filiere) {
        showResult('modifyResult', 'Error: All fields are required', true);
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
            showResult('modifyResult', 'SUCCESS: ' + result.message);
            chargerEtudiants();
        } else {
            showResult('modifyResult', 'ERROR: ' + result.error, true);
        }
    } catch (error) {
        showResult('modifyResult', 'Error: ' + error.message, true);
    }
}

async function supprimerEtudiant() {
    incrementRequests();

    const id = document.getElementById('modifyId').value;

    if (!id) {
        showResult('modifyResult', 'Error: Enter an ID', true);
        return;
    }

    if (!confirm(`Are you sure you want to delete student ID ${id}?`)) {
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
            showResult('modifyResult', 'SUCCESS: ' + result.message);
            document.getElementById('modifyForm').style.display = 'none';
            document.getElementById('modifyId').value = '';
            chargerEtudiants();
        } else {
            showResult('modifyResult', 'ERROR: ' + result.error, true);
        }
    } catch (error) {
        showResult('modifyResult', 'Error: ' + error.message, true);
    }
}

async function supprimerEtudiantDirect(id) {
    if (!confirm(`Delete student ID ${id}?`)) {
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
            alert('SUCCESS: ' + result.message);
            chargerEtudiants();
        } else {
            alert('ERROR: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
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

async function attaqueBruteForce() {
    incrementRequests();

    const passwords = ['123456', 'password', 'admin', 'password123', '12345678', 'qwerty'];
    let result = 'BRUTE FORCE ATTACK - Password Guessing\n';
    result += '================================================\n\n';

    showResult('bruteForceResult', result + 'Testing in progress...');

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
                result += `SUCCESS! Password found: ${pwd}\n\n`;
                result += `Impact: Unauthorized system access\n`;
                result += `Countermeasure: Rate limiting, CAPTCHA, 2FA\n`;
                showResult('bruteForceResult', result);

                // Nettoyer en supprimant l'étudiant test
                try {
                    await fetch(`${API}/999`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': 'Basic ' + btoa('admin:password123')
                        }
                    });
                } catch (e) {}

                return;
            } else {
                result += `Failed: ${pwd}\n`;
            }
        } catch (error) {
            result += `Failed: ${pwd}\n`;
        }

        showResult('bruteForceResult', result);
        await new Promise(resolve => setTimeout(resolve, 300));
    }

    result += '\nNo password found in list\n';
    showResult('bruteForceResult', result);
}

async function attaqueSQL() {
    incrementRequests();

    const payload = document.getElementById('sqlPayload').value;

    let result = 'SQL INJECTION ATTACK\n';
    result += '================================================\n\n';
    result += `Payload: ${payload}\n\n`;

    try {
        const response = await fetch('http://127.0.0.1:5050/api/debug/sql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: payload })
        });

        const data = await response.json();
        result += `Server Response:\n`;
        result += `{\n`;
        result += `  "query": "${data.query}",\n`;
        result += `  "result": "${data.result}",\n`;
        result += `  "warning": "${data.warning}"\n`;
        result += `}\n\n`;
        result += `Impact: Database manipulation\n`;
        result += `Countermeasure: Prepared statements, strict validation\n`;

        showResult('sqlResult', result);
    } catch (error) {
        showResult('sqlResult', 'Error: Server not responding\nMake sure the REST server is running on port 5050', true);
    }
}

async function attaqueXSS() {
    incrementRequests();

    const payload = document.getElementById('xssPayload').value;

    let result = 'CROSS-SITE SCRIPTING (XSS) ATTACK\n';
    result += '================================================\n\n';
    result += `Payload: ${payload}\n\n`;

    try {
        const response = await fetch('http://127.0.0.1:5050/api/debug/xss', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: payload })
        });

        const data = await response.json();
        result += `Server Response:\n`;
        result += `{\n`;
        result += `  "html": "${data.html.replace(/</g, '&lt;').replace(/>/g, '&gt;')}",\n`;
        result += `  "warning": "${data.warning}"\n`;
        result += `}\n\n`;

        // DANGER: Injection directe pour démonstration
        document.getElementById('xssZone').innerHTML = data.html;

        result += `WARNING: Code injected in zone below!\n`;
        result += `Impact: Session theft, phishing, malware\n`;
        result += `Countermeasure: HTML escaping, CSP\n`;

        showResult('xssResult', result);
    } catch (error) {
        showResult('xssResult', 'Error: Server not responding\nMake sure the REST server is running on port 5050', true);
    }
}

async function attaqueDoS() {
    incrementRequests();

    const count = parseInt(document.getElementById('dosCount').value) || 50;

    let result = 'DENIAL OF SERVICE (DoS) ATTACK\n';
    result += '================================================\n\n';
    result += `Sending ${count} rapid requests...\n\n`;

    showResult('dosResult', result + 'Attack in progress...');

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

    result += `Successful requests: ${success}\n`;
    result += `Failed requests: ${failed}\n`;
    result += `Total duration: ${duration} seconds\n`;
    result += `Throughput: ${(count / duration).toFixed(2)} req/s\n\n`;
    result += `Impact: Server overload, service unavailability\n`;
    result += `Countermeasure: Rate limiting, CDN, CAPTCHA\n`;

    showResult('dosResult', result);
}

async function attaqueIDOR() {
    incrementRequests();

    const range = document.getElementById('idorRange').value;
    const [start, end] = range.split('-').map(Number);

    if (!start || !end) {
        showResult('idorResult', 'Error: Invalid format. Use: 1-10', true);
        return;
    }

    let result = 'IDOR ATTACK - Insecure Direct Object Reference\n';
    result += '================================================\n\n';
    result += `Enumerating IDs from ${start} to ${end}...\n\n`;

    showResult('idorResult', result + 'Scan in progress...');

    for (let id = start; id <= end; id++) {
        try {
            const response = await fetch(`${API}/${id}`);

            if (response.ok) {
                const etudiant = await response.json();
                result += `FOUND ID ${id}: ${etudiant.prenom} ${etudiant.nom} (${etudiant.filiere})\n`;
            } else {
                result += `NOT FOUND ID ${id}\n`;
            }
        } catch (error) {
            result += `ERROR ID ${id}\n`;
        }

        showResult('idorResult', result);
        await new Promise(resolve => setTimeout(resolve, 200));
    }

    result += `\nImpact: Access to unauthorized data\n`;
    result += `Countermeasure: UUIDs, permission verification\n`;

    showResult('idorResult', result);
}

function verifierHTTPS() {
    let result = 'HTTPS VERIFICATION\n';
    result += '================================================\n\n';

    const protocol = window.location.protocol;
    const apiProtocol = new URL(API).protocol;

    result += `Page protocol: ${protocol}\n`;
    result += `API protocol: ${apiProtocol}\n\n`;

    if (protocol === 'http:' || apiProtocol === 'http:') {
        result += `VULNERABLE: Unencrypted communication\n\n`;
        result += `Data transmitted in CLEAR TEXT:\n`;
        result += `- Login credentials\n`;
        result += `- Personal data\n`;
        result += `- Session cookies\n\n`;
        result += `Impact: Interception (Man-in-the-Middle)\n`;
        result += `Countermeasure: Mandatory HTTPS, HSTS\n`;
    } else {
        result += `SECURE: Encrypted communication\n`;
    }

    showResult('httpsResult', result);
}

window.addEventListener('load', () => {
    verifierServeur();
    chargerEtudiants();
    setInterval(verifierServeur, 30000);
});