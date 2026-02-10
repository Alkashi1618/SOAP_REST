from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import GestionEtudiants, Etudiant

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

gestion = GestionEtudiants()

USERS = {
    "admin": "password123",
    "user": "user123"
}

@auth.verify_password
def verify_password(username, password):
    if username in USERS and USERS[username] == password:
        return username
    return None


@app.route('/')
def index():
    return jsonify({
        "message": "API REST de gestion des etudiants",
        "endpoints": {
            "GET /api/etudiants": "Lister tous les etudiants",
            "GET /api/etudiants/<id>": "Obtenir un etudiant",
            "GET /api/etudiants/filiere/<filiere>": "Rechercher par filiere",
            "POST /api/etudiants": "Ajouter un etudiant (auth requise)",
            "PUT /api/etudiants/<id>": "Modifier un etudiant (auth requise)",
            "DELETE /api/etudiants/<id>": "Supprimer un etudiant (auth requise)"
        }
    })


@app.route('/api/etudiants', methods=['GET'])
def get_all_etudiants():
    etudiants = gestion.lister_tous()
    return jsonify([e.to_dict() for e in etudiants])


@app.route('/api/etudiants/<int:id>', methods=['GET'])
def get_etudiant(id):
    etudiant = gestion.obtenir_etudiant(id)
    if etudiant:
        return jsonify(etudiant.to_dict())
    return jsonify({"error": "Etudiant non trouve"}), 404


@app.route('/api/etudiants/filiere/<string:filiere>', methods=['GET'])
def get_by_filiere(filiere):
    etudiants = gestion.rechercher_par_filiere(filiere)
    return jsonify([e.to_dict() for e in etudiants])


@app.route('/api/etudiants', methods=['POST'])
@auth.login_required
def add_etudiant():
    data = request.get_json()
    
    if not all(k in data for k in ['id', 'nom', 'prenom', 'filiere']):
        return jsonify({"error": "Donnees incompletes"}), 400
    
    etudiant = Etudiant(
        data['id'],
        data['nom'],
        data['prenom'],
        data['filiere']
    )
    
    if gestion.ajouter(etudiant):
        return jsonify({"message": "Etudiant ajoute avec succes"}), 201
    return jsonify({"error": "Etudiant existe deja"}), 409


@app.route('/api/etudiants/<int:id>', methods=['PUT'])
@auth.login_required
def update_etudiant(id):
    data = request.get_json()
    
    if not all(k in data for k in ['nom', 'prenom', 'filiere']):
        return jsonify({"error": "Donnees incompletes"}), 400
    
    if gestion.modifier(id, data['nom'], data['prenom'], data['filiere']):
        return jsonify({"message": "Etudiant modifie avec succes"})
    return jsonify({"error": "Etudiant non trouve"}), 404


@app.route('/api/etudiants/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_etudiant(id):
    if gestion.supprimer(id):
        return jsonify({"message": "Etudiant supprime avec succes"})
    return jsonify({"error": "Etudiant non trouve"}), 404


@app.route('/api/debug/sql', methods=['POST'])
def vulnerable_sql():
    data = request.get_json()
    query = data.get('query', '')
    return jsonify({
        "warning": "Endpoint vulnerable a l'injection SQL",
        "query": query,
        "result": f"Execution de: {query}"
    })


@app.route('/api/debug/xss', methods=['POST'])
def vulnerable_xss():
    data = request.get_json()
    user_input = data.get('input', '')
    return jsonify({
        "warning": "Endpoint vulnerable au XSS",
        "html": f"<div>{user_input}</div>"
    })


if __name__ == '__main__':
    print(">>> SERVEUR REST EN COURS DE DEMARRAGE")
    app.run(
        host='127.0.0.1',
        port=5050,
        debug=False,
        use_reloader=False
    )


