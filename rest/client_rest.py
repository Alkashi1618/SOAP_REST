import requests
from requests.auth import HTTPBasicAuth
import json

class ClientREST:
    def __init__(self, base_url='http://127.0.0.1:5050', username=None, password=None):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password) if username and password else None
    
    def get_all_etudiants(self):
        response = requests.get(f"{self.base_url}/api/etudiants")
        return response.json()
    
    def get_etudiant(self, id):
        response = requests.get(f"{self.base_url}/api/etudiants/{id}")
        return response.json()
    
    def add_etudiant(self, id, nom, prenom, filiere):
        data = {
            'id': id,
            'nom': nom,
            'prenom': prenom,
            'filiere': filiere
        }
        response = requests.post(
            f"{self.base_url}/api/etudiants",
            json=data,
            auth=self.auth
        )
        return response.json()
    
    def update_etudiant(self, id, nom, prenom, filiere):
        data = {
            'nom': nom,
            'prenom': prenom,
            'filiere': filiere
        }
        response = requests.put(
            f"{self.base_url}/api/etudiants/{id}",
            json=data,
            auth=self.auth
        )
        return response.json()
    
    def delete_etudiant(self, id):
        response = requests.delete(
            f"{self.base_url}/api/etudiants/{id}",
            auth=self.auth
        )
        return response.json()
    
    def search_by_filiere(self, filiere):
        response = requests.get(f"{self.base_url}/api/etudiants/filiere/{filiere}")
        return response.json()


def main():
    print("TEST DU CLIENT REST")
    print("=" * 50)
    
    client = ClientREST()
    
    print("\n1. Lister tous les etudiants:")
    etudiants = client.get_all_etudiants()
    for e in etudiants:
        print(f"  ID {e['id']}: {e['prenom']} {e['nom']} - {e['filiere']}")
    
    print("\n2. Obtenir l'etudiant ID 1:")
    etudiant = client.get_etudiant(1)
    print(f"  {etudiant}")
    
    print("\n3. Rechercher par filiere (Informatique):")
    etudiants = client.search_by_filiere("Informatique")
    print(f"  {len(etudiants)} etudiant(s) trouve(s)")
    
    client_auth = ClientREST(username='admin', password='password123')
    
    print("\n4. Ajouter un etudiant (avec authentification):")
    result = client_auth.add_etudiant(10, "Kane", "Ibrahima", "Chimie")
    print(f"  {result}")
    
    print("\n5. Modifier l'etudiant ID 10:")
    result = client_auth.update_etudiant(10, "Kane", "Ibrahima", "Biologie")
    print(f"  {result}")
    
    print("\n6. Supprimer l'etudiant ID 10:")
    result = client_auth.delete_etudiant(10)
    print(f"  {result}")
    
    print("\n" + "=" * 50)
    print("TESTS TERMINES")


if __name__ == '__main__':
    main()
