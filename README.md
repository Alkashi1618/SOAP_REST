# PROJET GESTION DES ETUDIANTS - API SOAP ET REST

## Description

Projet complet d'implementation d'APIs SOAP et REST pour la gestion des etudiants avec demonstrations de vulnerabilites de securite a des fins educatives.

## Structure du projet

```
api_students_project/
|-- main.py                  # Script de lancement principal
|-- models.py                # Classes Etudiant et GestionEtudiants
|-- etudiants.json          # Base de donnees JSON
|-- requirements.txt         # Dependances Python
|
|-- rest/
|   |-- api_rest.py         # Serveur Flask REST
|   |-- client_rest.py      # Client de test REST
|
|-- soap/
|   |-- api_soap.py         # Serveur Spyne SOAP
|   |-- client_soap.py      # Client de test SOAP
|
|-- attacks/
    |-- attaques_rest.py    # Demonstrations attaques REST
    |-- attaques_soap.py    # Demonstrations attaques SOAP
```

## Installation

### Etape 1: Installer les dependances

```bash
pip install -r requirements.txt
```

### Etape 2: Verifier l'installation

```bash
python -c "import flask, spyne, zeep; print('Installation OK')"
```

## Utilisation

### Methode 1: Menu interactif (RECOMMANDE)

```bash
python main.py
```

Puis choisir:
- Option 1: Demarrer le serveur REST
- Option 2: Demarrer le serveur SOAP
- Option 3-4: Tester les clients
- Option 5-6: Voir les attaques

### Methode 2: Lancement manuel

#### Terminal 1 - Serveur REST
```bash
python rest/api_rest.py
```

#### Terminal 2 - Serveur SOAP
```bash
python soap/api_soap.py
```

#### Terminal 3 - Tests
```bash
python rest/client_rest.py
python soap/client_soap.py
```

## API REST

### Informations
- Port: 5000
- URL: http://localhost:5000
- Format: JSON
- Auth: HTTP Basic Auth

### Endpoints

| Methode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | /api/etudiants | Liste tous les etudiants | Non |
| GET | /api/etudiants/<id> | Obtenir un etudiant | Non |
| GET | /api/etudiants/filiere/<filiere> | Rechercher par filiere | Non |
| POST | /api/etudiants | Ajouter un etudiant | Oui |
| PUT | /api/etudiants/<id> | Modifier un etudiant | Oui |
| DELETE | /api/etudiants/<id> | Supprimer un etudiant | Oui |

### Authentification
- Username: admin / Password: password123
- Username: user / Password: user123

### Exemples

Lister tous les etudiants:
```bash
curl http://localhost:5000/api/etudiants
```

Ajouter un etudiant:
```bash
curl -X POST http://localhost:5000/api/etudiants \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "nom": "Kane", "prenom": "Ibrahima", "filiere": "Chimie"}'
```

## API SOAP

### Informations
- Port: 8000
- URL: http://localhost:8000
- WSDL: http://localhost:8000/?wsdl
- Format: XML/SOAP

### Methodes disponibles

| Methode | Parametres | Description |
|---------|-----------|-------------|
| obtenir_etudiant | id (int) | Obtenir un etudiant |
| lister_etudiants | - | Lister tous |
| ajouter_etudiant | id, nom, prenom, filiere | Ajouter |
| modifier_etudiant | id, nom, prenom, filiere | Modifier |
| supprimer_etudiant | id | Supprimer |
| rechercher_par_filiere | filiere | Rechercher |

### Exemple Python

```python
from zeep import Client

client = Client('http://localhost:8000/?wsdl')
print(client.service.lister_etudiants())
print(client.service.obtenir_etudiant(1))
```

## Demonstrations d'attaques

AVERTISSEMENT: Ces demonstrations sont UNIQUEMENT A DES FINS EDUCATIVES.

### Attaques REST

```bash
python attacks/attaques_rest.py
```

Vulnerabilites demonstrees:
1. Brute Force - Attaque authentification
2. Injection SQL - Injection de code SQL
3. XSS - Cross-Site Scripting
4. DoS - Deni de Service
5. IDOR - Insecure Direct Object Reference
6. Absence de HTTPS - Communication non chiffree

### Attaques SOAP

```bash
python attacks/attaques_soap.py
```

Vulnerabilites demonstrees:
1. XXE - XML External Entity Injection
2. XML Bomb - Billion Laughs Attack
3. SOAP Injection - Injection de code SOAP
4. WSDL Enumeration - Enumeration des methodes
5. Parameter Tampering - Modification de parametres
6. Replay Attack - Repetition de requetes

## Contremesures de securite

### Pour REST
- Brute Force: Rate limiting, CAPTCHA, 2FA
- Injection SQL: Requetes preparees, ORM, validation
- XSS: Echappement HTML, CSP
- DoS: Rate limiting, CDN
- IDOR: UUIDs, verification autorisations
- HTTP: HTTPS obligatoire, HSTS

### Pour SOAP
- XXE: Desactiver entites externes XML
- XML Bomb: Limiter taille et profondeur XML
- SOAP Injection: Validation stricte, echappement
- WSDL Enumeration: Restreindre acces WSDL
- Parameter Tampering: Validation stricte
- Replay Attack: WS-Security, timestamps, nonces

## Donnees de test

Le fichier etudiants.json contient 3 etudiants:
- ID 1: Diop Amadou (Informatique)
- ID 2: Ndiaye Fatou (Mathematiques)
- ID 3: Sall Moussa (Physique)

## Troubleshooting

### Port deja utilise
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Module non trouve
```bash
pip install -r requirements.txt --upgrade
```

### Serveur ne demarre pas
Verifier que:
- Python 3.8+ est installe
- Toutes les dependances sont installees
- Les ports 5000 et 8000 sont libres

## Technologies utilisees

- Python 3.8+
- Flask - Framework REST
- Spyne - Framework SOAP
- Zeep - Client SOAP
- Requests - Client HTTP

## Licence

Projet educatif - Licence MIT

## Avertissement final

NE JAMAIS utiliser ce code en production sans corriger toutes les vulnerabilites.
Les failles de securite sont intentionnelles a des fins pedagogiques uniquement.
