# 🎓 Projet Gestion des Étudiants - API SOAP & REST

Projet complet d'implémentation d'APIs SOAP et REST pour la gestion des étudiants, avec démonstrations de vulnérabilités de sécurité à des fins éducatives.

---

## 📋 Table des matières

1. [Description](#description)
2. [Structure du projet](#structure-du-projet)
3. [Prérequis](#prérequis)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [API REST](#api-rest)
7. [API SOAP](#api-soap)
8. [Démonstrations d'attaques](#démonstrations-dattaques)
9. [Contremesures de sécurité](#contremesures-de-sécurité)
10. [Auteur](#auteur)

---

## 📖 Description

Ce projet implémente deux types d'APIs pour gérer une base de données d'étudiants :

- **API REST** (Flask) : Architecture moderne avec opérations CRUD
- **API SOAP** (Spyne) : Architecture traditionnelle basée sur XML

Le projet inclut également des **démonstrations de vulnérabilités** pour comprendre les risques de sécurité et leurs contremesures.

### ⚠️ Avertissement

Les vulnérabilités présentes dans ce projet sont **INTENTIONNELLES** et à des **FINS ÉDUCATIVES UNIQUEMENT**. Ne jamais utiliser ce code en production sans corriger toutes les failles de sécurité.

---

## 📁 Structure du projet

```
api_students_project/
│
├── main.py                     # Script de lancement principal
├── models.py                   # Modèle de données (Etudiant, GestionEtudiants)
├── etudiants.json             # Base de données JSON
├── requirements.txt            # Dépendances Python
│
├── rest/                       # API REST
│   ├── api_rest.py            # Serveur Flask REST
│   └── client_rest.py         # Client de test REST
│
├── soap/                       # API SOAP
│   ├── api_soap.py            # Serveur Spyne SOAP
│   └── client_soap.py         # Client de test SOAP
│
├── attacks/                    # Démonstrations d'attaques
│   ├── attaques_rest.py       # Attaques sur API REST
│   └── attaques_soap.py       # Attaques sur API SOAP
│
└── docs/                       # Documentation supplémentaire
```

---

## 🔧 Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **Connexion Internet** (pour installer les dépendances)

---

## 📦 Installation

### 1. Cloner ou télécharger le projet

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
- pytest (tests)

---

## 🚀 Utilisation

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

---

## 🌐 API REST

### Informations

- **Port :** 5000
- **URL de base :** http://localhost:5000
- **Format :** JSON
- **Authentification :** HTTP Basic Auth

### Endpoints

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/etudiants` | Liste tous les étudiants | Non |
| GET | `/api/etudiants/<id>` | Obtenir un étudiant | Non |
| GET | `/api/etudiants/filiere/<filiere>` | Rechercher par filière | Non |
| POST | `/api/etudiants` | Ajouter un étudiant | Oui |
| PUT | `/api/etudiants/<id>` | Modifier un étudiant | Oui |
| DELETE | `/api/etudiants/<id>` | Supprimer un étudiant | Oui |

### Authentification

**Identifiants de test :**
- Username: `admin` / Password: `password123`
- Username: `user` / Password: `user123`

### Exemples d'utilisation

**1. Lister tous les étudiants :**
```bash
curl http://localhost:5000/api/etudiants
```

**2. Obtenir un étudiant :**
```bash
curl http://localhost:5000/api/etudiants/1
```

**3. Ajouter un étudiant :**
```bash
curl -X POST http://localhost:5000/api/etudiants \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "nom": "Sow", "prenom": "Ibrahima", "filiere": "Mathématiques"}'
```

**4. Modifier un étudiant :**
```bash
curl -X PUT http://localhost:5000/api/etudiants/10 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"nom": "Sow", "prenom": "Ibrahima", "filiere": "Physique"}'
```

**5. Supprimer un étudiant :**
```bash
curl -X DELETE http://localhost:5000/api/etudiants/10 \
  -u admin:password123
```

### Utilisation avec Python

```python
from rest.client_rest import ClientREST

# Sans authentification
client = ClientREST()
etudiants = client.get_all_etudiants()
print(etudiants)

# Avec authentification
client_auth = ClientREST(username="admin", password="password123")
result = client_auth.add_etudiant(10, "Sow", "Ibrahima", "Maths")
```

---

## 🧼 API SOAP

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

### Exemples d'utilisation

**Avec Python (Zeep) :**

```python
from zeep import Client

client = Client('http://localhost:8000/?wsdl')

# Lister tous les étudiants
print(client.service.lister_etudiants())

# Obtenir un étudiant
print(client.service.obtenir_etudiant(1))

# Ajouter un étudiant
print(client.service.ajouter_etudiant(20, "Kane", "Moussa", "Électronique"))

# Rechercher par filière
print(client.service.rechercher_par_filiere("CI"))
```

**Avec SoapUI ou Postman :**

1. Importer le WSDL : http://localhost:8000/?wsdl
2. Utiliser les méthodes disponibles
3. Format de requête SOAP :

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <obtenir_etudiant xmlns="gestion.etudiants.soap">
      <id>1</id>
    </obtenir_etudiant>
  </soap:Body>
</soap:Envelope>
```

---

## 🔴 Démonstrations d'attaques

### ⚠️ AVERTISSEMENT IMPORTANT

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

## 🛡️ Contremesures de sécurité

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

### Bonnes pratiques générales

✅ **Authentification et autorisation**
- Utiliser des tokens JWT ou OAuth2
- Vérifier les permissions pour chaque opération
- Implémenter le principe du moindre privilège

✅ **Validation des données**
- Valider toutes les entrées utilisateur
- Utiliser des schémas de validation (JSON Schema, XSD)
- Rejeter les données invalides, ne pas les corriger

✅ **Chiffrement**
- HTTPS obligatoire (TLS 1.2+)
- Chiffrer les données sensibles en base
- Ne jamais stocker les mots de passe en clair

✅ **Logging et monitoring**
- Logger toutes les opérations sensibles
- Détecter les comportements anormaux
- Mettre en place des alertes

✅ **Mise à jour**
- Maintenir les dépendances à jour
- Appliquer les patches de sécurité
- Scanner les vulnérabilités régulièrement

---

## 🧪 Tests

### Tester l'API REST

```bash
python rest/client_rest.py
```

### Tester l'API SOAP

```bash
python soap/client_soap.py
```

### Lancer tous les tests

```bash
python main.py
# Choisir l'option 7
```

---

## 📚 Ressources supplémentaires

### Documentation officielle

- [Flask](https://flask.palletsprojects.com/)
- [Spyne](http://spyne.io/)
- [Zeep](https://docs.python-zeep.org/)

### Sécurité

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [SOAP Security](https://www.w3.org/TR/soap12-part0/)

### Outils de test

- [Postman](https://www.postman.com/) - Test d'APIs REST
- [SoapUI](https://www.soapui.org/) - Test d'APIs SOAP
- [Burp Suite](https://portswigger.net/burp) - Test de sécurité

---

## 🎯 Exercices pratiques

### Niveau débutant
1. Ajouter un nouveau champ "email" aux étudiants
2. Créer un endpoint pour compter les étudiants par filière
3. Implémenter une recherche par nom

### Niveau intermédiaire
1. Corriger les vulnérabilités de sécurité
2. Implémenter l'authentification JWT
3. Ajouter une pagination aux listes

### Niveau avancé
1. Créer une API GraphQL
2. Implémenter un cache Redis
3. Ajouter des tests unitaires avec pytest
4. Dockeriser l'application

---

## 🤝 Contribution

Ce projet est à des fins éducatives. N'hésitez pas à :
- Corriger les bugs
- Améliorer la sécurité
- Ajouter des fonctionnalités
- Améliorer la documentation

---

## 📝 Licence

Ce projet est sous licence MIT - libre d'utilisation à des fins éducatives.

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre de l'apprentissage des APIs SOAP et REST, avec focus sur la sécurité applicative.

---

## ❓ FAQ

**Q: Les serveurs ne démarrent pas, pourquoi ?**
R: Vérifiez que les ports 5000 et 8000 ne sont pas déjà utilisés. Utilisez `netstat -ano | findstr :5000` (Windows) ou `lsof -i :5000` (Linux/Mac).

**Q: Comment changer les ports ?**
R: Modifiez `port=5000` dans `api_rest.py` et `make_server('0.0.0.0', 8000, ...)` dans `api_soap.py`.

**Q: Les attaques ne fonctionnent pas**
R: C'est normal ! Certaines vulnérabilités sont atténuées par les bibliothèques modernes. L'objectif est pédagogique.

**Q: Puis-je utiliser ce code en production ?**
R: **NON !** Ce code contient des vulnérabilités intentionnelles. Corrigez toutes les failles avant toute utilisation réelle.

**Q: Comment ajouter HTTPS ?**
R: Utilisez un certificat SSL/TLS et configurez Flask avec `ssl_context`. Pour la production, utilisez un reverse proxy (nginx, Apache).

---

## 🎓 Apprentissages clés

Après ce projet, vous devriez comprendre :

✅ La différence entre REST et SOAP
✅ Comment créer des APIs avec Flask et Spyne
✅ Les vulnérabilités web courantes (OWASP Top 10)
✅ L'importance de la sécurité dès la conception
✅ Comment tester et sécuriser une API

---

**Bon apprentissage ! 🚀**


# 🎨 Interface Web - Gestion des Étudiants



Interface web moderne pour interagir avec l'API REST et démontrer les vulnérabilités de sécurité.

## 🚀 Démarrage

### Prérequis
Le serveur REST doit être démarré sur le port 5050 :
```bash
python rest/api_rest.py
```

### Lancement
1. Ouvrir `index.html` dans un navigateur web
2. Ou utiliser un serveur local :
```bash
# Python 3
python -m http.server 8080

# Puis ouvrir: http://localhost:8080
```

## 📋 Fonctionnalités

### Onglet Gestion
- ✅ **Liste des étudiants** - Affichage en temps réel
- ✅ **Ajouter un étudiant** - Formulaire avec authentification
- ✅ **Rechercher** - Par ID ou par filière
- ✅ **Modifier** - Modification inline
- ✅ **Supprimer** - Avec confirmation
- ✅ **Exporter JSON** - Télécharger les données

### Onglet Attaques
Démonstrations interactives de 6 vulnérabilités :

1. **🔐 Brute Force**
   - Tentative de deviner le mot de passe
   - Animation en temps réel

2. **💉 Injection SQL**
   - Payloads personnalisables
   - Affichage de la réponse serveur

3. **💥 Cross-Site Scripting (XSS)**
   - Injection de code JavaScript
   - Zone d'exécution du code injecté

4. **⚡ Déni de Service (DoS)**
   - Configuration du nombre de requêtes
   - Statistiques de performance

5. **🔓 IDOR**
   - Énumération d'IDs
   - Plage personnalisable

6. **🔒 Absence HTTPS**
   - Vérification du protocole
   - Explication des risques

### Onglet Documentation
- 📡 Liste des endpoints API
- 🔑 Identifiants d'authentification
- 🛡️ Liste des vulnérabilités
- 📚 Liens vers les ressources

## 🎨 Caractéristiques

### Design
- 🎨 Interface moderne et responsive
- 🌈 Thème violet dégradé
- 📱 Compatible mobile
- ⚡ Animations fluides

### Expérience Utilisateur
- ✅ Vérification du serveur en temps réel
- 📊 Statistiques dynamiques
- 🔄 Actualisation automatique
- ⚠️ Messages d'erreur clairs
- 💾 Sauvegarde locale possible

### Sécurité
- ⚠️ Avertissements sur les attaques
- 🔐 Authentification HTTP Basic
- 🛡️ Démonstrations éducatives uniquement

## 🔧 Configuration

### Modifier l'URL de l'API

Dans `app.js`, ligne 1 :
```javascript
const API = "http://127.0.0.1:5050/api/etudiants";
```

Changez le port si nécessaire.

### Authentification

Identifiants par défaut :
- Username: `admin`
- Password: `password123`

Ou :
- Username: `user`
- Password: `user123`

## 📊 Statistiques Affichées

- **Total Étudiants** - Nombre total dans la base
- **Total Filières** - Nombre de filières différentes
- **Total Requêtes** - Compteur de requêtes depuis le chargement

## 🎯 Utilisation

### Ajouter un étudiant

1. Aller dans l'onglet "Gestion"
2. Remplir le formulaire "Ajouter un étudiant"
3. Cliquer sur "✅ Ajouter"
4. L'authentification est automatique

### Lancer une attaque

1. Aller dans l'onglet "Attaques"
2. Choisir le type d'attaque
3. Personnaliser les paramètres si nécessaire
4. Cliquer sur le bouton correspondant
5. Observer les résultats en temps réel

### Modifier un étudiant

**Méthode 1 :** Depuis la liste
- Cliquer sur ✏️ à côté de l'étudiant

**Méthode 2 :** Via le formulaire
- Entrer l'ID dans "Modifier / Supprimer"
- Cliquer sur "Charger"
- Modifier les champs
- Cliquer sur "💾 Modifier"

## 🔍 Détails Techniques

### Technologies
- HTML5
- CSS3 (inline)
- JavaScript (Vanilla - pas de framework)
- Fetch API
- Async/Await

### Structure des fichiers
```
frontend/
├── index.html  # Interface complète
├── app.js      # Logique JavaScript
└── README.md   # Ce fichier
```

### API Endpoints utilisés

```
GET    /api/etudiants              # Liste
GET    /api/etudiants/:id          # Un étudiant
GET    /api/etudiants/filiere/:f   # Par filière
POST   /api/etudiants              # Ajouter
PUT    /api/etudiants/:id          # Modifier
DELETE /api/etudiants/:id          # Supprimer
POST   /api/debug/sql              # Test SQL
POST   /api/debug/xss              # Test XSS
```

## ⚠️ Avertissements

1. **Attaques** - Uniquement à des fins éducatives
2. **HTTPS** - L'API utilise HTTP (non sécurisé)
3. **Authentification** - HTTP Basic (faible)
4. **Production** - Ne JAMAIS utiliser tel quel

## 💡 Améliorations Possibles

- [ ] Ajout de HTTPS
- [ ] Authentification JWT
- [ ] Pagination de la liste
- [ ] Filtres avancés
- [ ] Export PDF
- [ ] Mode sombre
- [ ] Graphiques de statistiques
- [ ] Historique des modifications

## 🐛 Problèmes Courants

**Le serveur ne répond pas**
- Vérifier que `python rest/api_rest.py` est lancé
- Vérifier le port (5050 par défaut)
- Consulter la console du navigateur (F12)

**CORS Errors**
- Le serveur Flask a CORS activé
- Si problème persiste, vérifier Flask-CORS

**Attaques ne fonctionnent pas**
- Vérifier que les endpoints `/api/debug/*` existent
- Consulter la console du navigateur

## 📞 Support

Consultez :
- `../README.md` - Documentation principale
- `../TROUBLESHOOTING.md` - Dépannage
- Console du navigateur (F12) - Erreurs JavaScript

---

**Interface créée pour le projet Gestion des Étudiants - API SOAP & REST**