const API = "http://127.0.0.1:5050/api/etudiants";

/* ===== NORMAL ===== */
function chargerEtudiants() {
    fetch(API)
        .then(res => res.json())
        .then(data => {
            const liste = document.getElementById("liste");
            liste.innerHTML = "";
            data.forEach(e => {
                const li = document.createElement("li");
                li.textContent = `${e.id} - ${e.prenom} ${e.nom} (${e.filiere})`;
                liste.appendChild(li);
            });
        });
}

/* ===== IDOR ===== */
function testerIDOR() {
    const id = document.getElementById("idorId").value;
    fetch(`${API}/${id}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("idorResult").innerText =
                JSON.stringify(data, null, 2);
        });
}

/* ===== ADD ===== */
function ajouterEtudiant() {
    const etudiant = {
        id: parseInt(document.getElementById("id").value),
        nom: document.getElementById("nom").value,
        prenom: document.getElementById("prenom").value,
        filiere: document.getElementById("filiere").value
    };

    fetch(API, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Basic " + btoa("admin:password123")
        },
        body: JSON.stringify(etudiant)
    })
    .then(res => res.json())
    .then(() => chargerEtudiants());
}

/* ===== XSS ===== */
function attaqueXSS() {
    const payload = document.getElementById("xssInput").value;

    fetch("http://127.0.0.1:5050/api/debug/xss", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: payload })
    })
    .then(res => res.json())
    .then(data => {
        // ⚠️ Injection directe = XSS
        document.getElementById("xssZone").innerHTML = data.html;
    });
}

/* ===== BRUTE FORCE ===== */
function bruteForce() {
    const passwords = ["123456", "password", "admin", "password123"];
    let output = "";

    passwords.forEach(pwd => {
        output += `Tentative admin / ${pwd}\n`;
    });

    document.getElementById("bruteResult").innerText = output;
}
