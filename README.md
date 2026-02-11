# Système de Gestion des Étudiants - APIs SOAP & REST

Implémentation complète d'APIs SOAP et REST pour la gestion des étudiants, avec démonstrations de vulnérabilités de sécurité à des fins éducatives.

---

## Table des Matières

1. [Description](#description)
2. [Structure du Projet](#structure-du-projet)
3. [Prérequis](#prérequis)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [API REST](#api-rest)
7. [API SOAP](#api-soap)
8. [Démonstrations de Sécurité](#démonstrations-de-sécurité)
9. [Contremesures](#contremesures)

---

## Description

Ce projet implémente deux types d'APIs pour gérer une base de données d'étudiants :

- **API REST** (Flask) : Architecture moderne avec opérations CRUD
- **API SOAP** (Spyne) : Architecture traditionnelle basée sur XML

Le projet inclut également des **démonstrations de vulnérabilités** pour comprendre les risques de sécurité et leurs contremesures.

### AVERTISSEMENT

Les vulnérabilités présentes dans ce projet sont **INTENTIONNELLES** et à des **FINS ÉDUCATIVES UNIQUEMENT**. Ne jamais utiliser ce code en production sans corriger toutes les failles de sécurité.

---

## Structure du Projet

```
api_students_project/
|
|-- main.py                     # Script de lancement principal
|-- models.py                   # Modèle de données
|-- etudiants.json             # Base de données JSON
|-- requirements.txt            # Dépendances Python
|
|-- rest/                       # API REST
|   |-- api_rest.py            # Serveur Flask REST
|   |-- client_rest.py         # Client de test REST
|
|-- soap/                       # API SOAP
|   |-- api_soap.py            # Serveur Spyne SOAP
|   |-- client_soap.py         # Client de test SOAP
|
|-- attacks/                    # Démonstrations d'attaques
|   |-- attaques_rest.py       # Attaques REST
|   |-- attaques_soap.py       # Attaques SOAP
|
|-- frontend/                   # Interface Web
    |-- index.html             # Interface principale
    |-- app.js                 # Logique JavaScript
```

---

## Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **Connexion Internet** (pour installer les dépendances)

---

## Installation

### 1. Naviguer vers le répertoire du projet

```bash
cd api_students_project
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Dépendances installées :**
- Flask (API REST)
- Flask-CORS (gestion CORS)
- Flask-HTTPAuth (authentification)
- Zeep (client SOAP)
- Spyne (serveur SOAP)
- lxml (parsing XML)
- requests (requêtes HTTP)

---

## Utilisation

### Méthode 1 : Script principal (recommandé)

```bash
python main.py
```

Menu interactif pour :
- Démarrer les serveurs
- Tester les clients
- Lancer les démonstrations d'attaques

### Méthode 2 : Lancement manuel

**Terminal 1 - Serveur REST :**
```bash
python rest/api_rest.py
```

**Terminal 2 - Serveur SOAP :**
```bash
python soap/api_soap.py
```

**Terminal 3 - Tests :**
```bash
python rest/client_rest.py
python soap/client_soap.py
```

### Méthode 3 : Interface Web

```bash
python start_frontend.py
```

Cela va :
- Démarrer le serveur REST
- Ouvrir l'interface web dans votre navigateur

---

## API REST

### Informations

- **Port :** 5050
- **URL de base :** http://localhost:5050
- **Format :** JSON
- **Authentification :** HTTP Basic Auth

### Endpoints

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/etudiants` | Liste tous les étudiants | Non |
| GET | `/api/etudiants/<id>` | Obtenir un étudiant | Non |
| GET | `/api/etudiants/filiere/<dept>` | Rechercher par filière | Non |
| POST | `/api/etudiants` | Ajouter un étudiant | Oui |
| PUT | `/api/etudiants/<id>` | Modifier un étudiant | Oui |
| DELETE | `/api/etudiants/<id>` | Supprimer un étudiant | Oui |

### Authentification

**Identifiants de test :**
- Utilisateur: `admin` / Mot de passe: `password123`
- Utilisateur: `user` / Mot de passe: `user123`

### Exemples d'utilisation

**1. Lister tous les étudiants :**
```bash
curl http://localhost:5050/api/etudiants
```

**2. Obtenir un étudiant :**
```bash
curl http://localhost:5050/api/etudiants/1
```

**3. Ajouter un étudiant :**
```bash
curl -X POST http://localhost:5050/api/etudiants \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "nom": "Diop", "prenom": "Amadou", "filiere": "Informatique"}'
```

---

## API SOAP

### Informations

- **Port :** 8000
- **URL :** http://localhost:8000
- **WSDL :** http://localhost:8000/?wsdl
- **Format :** XML/SOAP

### Méthodes disponibles

| Méthode | Paramètres | Retour |
|---------|-----------|--------|
| `obtenir_etudiant` | id (int) | Informations de l'étudiant |
| `lister_etudiants` | - | Liste tous les étudiants |
| `ajouter_etudiant` | id, nom, prenom, filiere | Message de confirmation |
| `modifier_etudiant` | id, nom, prenom, filiere | Message de confirmation |
| `supprimer_etudiant` | id | Message de confirmation |
| `rechercher_par_filiere` | filiere | Étudiants de la filière |

---

## Démonstrations de Sécurité

### AVERTISSEMENT IMPORTANT

Ces démonstrations sont **UNIQUEMENT À DES FINS ÉDUCATIVES**. Elles montrent des vulnérabilités courantes pour vous apprendre à les identifier et les corriger.

### Attaques sur API REST

```bash
python attacks/attaques_rest.py
```

**Vulnérabilités démontrées :**

1. **Brute Force** - Attaque sur l'authentification
   - Tentative de deviner les mots de passe
   - Impact : Accès non autorisé au système

2. **Injection SQL** - Injection de code SQL
   - Exploitation d'une validation insuffisante
   - Impact : Accès à la base de données, manipulation de données

3. **Cross-Site Scripting (XSS)** - Injection de JavaScript
   - Absence d'échappement du contenu utilisateur
   - Impact : Vol de sessions, phishing

4. **Déni de Service (DoS)** - Surcharge du serveur
   - Envoi massif de requêtes
   - Impact : Indisponibilité du service

5. **IDOR** - Insecure Direct Object Reference
   - Énumération d'IDs prévisibles
   - Impact : Accès à des données non autorisées

6. **Absence de HTTPS** - Communication non chiffrée
   - Transmission de données en clair
   - Impact : Interception de données sensibles

### Attaques sur API SOAP

```bash
python attacks/attaques_soap.py
```

**Vulnérabilités démontrées :**

1. **XXE** - XML External Entity Injection
   - Exploitation d'entités XML externes
   - Impact : Lecture de fichiers locaux, SSRF

2. **XML Bomb** - Billion Laughs Attack
   - Expansion exponentielle XML
   - Impact : Déni de service, consommation mémoire

3. **SOAP Injection** - Injection de code SOAP
   - Validation insuffisante des paramètres
   - Impact : Manipulation de données

4. **WSDL Enumeration** - Énumération des méthodes
   - WSDL accessible publiquement
   - Impact : Découverte de l'architecture

5. **Parameter Tampering** - Modification de paramètres
   - Absence de validation stricte
   - Impact : Accès non autorisé

6. **Replay Attack** - Répétition de requêtes
   - Absence de nonce/timestamp
   - Impact : Rejeu d'opérations

---

## Contremesures

### Pour l'API REST

| Vulnérabilité | Contremesure |
|---------------|--------------|
| Brute Force | Rate limiting, CAPTCHA, authentification multifacteur |
| Injection SQL | Requêtes préparées, ORM, validation des entrées |
| XSS | Échappement HTML, Content Security Policy |
| DoS | Rate limiting, CAPTCHA, CDN |
| IDOR | UUIDs, vérification des autorisations |
| HTTP | HTTPS obligatoire, HSTS |

### Pour l'API SOAP

| Vulnérabilité | Contremesure |
|---------------|--------------|
| XXE | Désactiver les entités externes XML |
| XML Bomb | Limiter la taille et profondeur XML |
| SOAP Injection | Validation stricte, échappement XML |
| WSDL Enumeration | Restreindre l'accès au WSDL |
| Parameter Tampering | Validation et autorisation strictes |
| Replay Attack | WS-Security, timestamps, nonces |

### Bonnes Pratiques Générales

**Authentification et autorisation**
- Utiliser des tokens JWT ou OAuth2
- Vérifier les permissions pour chaque opération
- Implémenter le principe du moindre privilège

**Validation des données**
- Valider toutes les entrées utilisateur
- Utiliser des schémas de validation (JSON Schema, XSD)
- Rejeter les données invalides, ne pas les corriger

**Chiffrement**
- HTTPS obligatoire (TLS 1.2+)
- Chiffrer les données sensibles en base
- Ne jamais stocker les mots de passe en clair

**Logging et monitoring**
- Logger toutes les opérations sensibles
- Détecter les comportements anormaux
- Mettre en place des alertes

**Mise à jour**
- Maintenir les dépendances à jour
- Appliquer les patches de sécurité
- Scanner les vulnérabilités régulièrement

---

## Tests

### Tester l'API REST

```bash
python rest/client_rest.py
```

### Tester l'API SOAP

```bash
python soap/client_soap.py
```

---

## Ressources Supplémentaires

### Documentation officielle

- [Flask](https://flask.palletsprojects.com/)
- [Spyne](http://spyne.io/)
- [Zeep](https://docs.python-zeep.org/)

### Sécurité

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [SOAP Security](https://www.w3.org/TR/soap12-part0/)

---

## FAQ

**Q: Les serveurs ne démarrent pas, pourquoi ?**
R: Vérifiez que les ports 5050 et 8000 ne sont pas déjà utilisés.

**Q: Puis-je utiliser ce code en production ?**
R: **NON !** Ce code contient des vulnérabilités intentionnelles. Corrigez toutes les failles avant toute utilisation réelle.

**Q: Comment ajouter HTTPS ?**
R: Utilisez un certificat SSL/TLS et configurez Flask avec `ssl_context`. Pour la production, utilisez un reverse proxy (nginx, Apache).

---

## Licence

Ce projet est sous licence MIT - libre d'utilisation à des fins éducatives.

---

## Auteur

Projet réalisé dans le cadre de l'apprentissage des APIs SOAP et REST, avec focus sur la sécurité applicative.

---

**Projet éducatif - Utiliser de manière responsable**