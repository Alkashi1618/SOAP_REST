import subprocess
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\n" + "=" * 60)
    print("PROJET GESTION DES ETUDIANTS - API SOAP & REST")
    print("=" * 60)
    print("\n[SERVEURS]")
    print("1. Demarrer le serveur REST (port 5000)")
    print("2. Demarrer le serveur SOAP (port 8000)")
    print("\n[TESTS]")
    print("3. Tester le client REST")
    print("4. Tester le client SOAP")
    print("\n[ATTAQUES]")
    print("5. Demonstrations d'attaques REST")
    print("6. Demonstrations d'attaques SOAP")
    print("\n[AUTRES]")
    print("7. Afficher les informations du projet")
    print("0. Quitter")
    print("\n" + "=" * 60)

def start_rest_server():
    print("\nDemarrage du serveur REST...")
    print("URL: http://localhost:5000")
    print("Appuyez sur Ctrl+C pour arreter")
    print("-" * 60)
    try:
        subprocess.run([sys.executable, "rest/api_rest.py"])
    except KeyboardInterrupt:
        print("\nServeur arrete")

def start_soap_server():
    print("\nDemarrage du serveur SOAP...")
    print("URL: http://localhost:8000")
    print("WSDL: http://localhost:8000/?wsdl")
    print("Appuyez sur Ctrl+C pour arreter")
    print("-" * 60)
    try:
        subprocess.run([sys.executable, "soap/api_soap.py"])
    except KeyboardInterrupt:
        print("\nServeur arrete")

def test_rest_client():
    print("\nTest du client REST...")
    print("-" * 60)
    subprocess.run([sys.executable, "rest/client_rest.py"])
    input("\nAppuyez sur Entree pour continuer...")

def test_soap_client():
    print("\nTest du client SOAP...")
    print("-" * 60)
    subprocess.run([sys.executable, "soap/client_soap.py"])
    input("\nAppuyez sur Entree pour continuer...")

def run_rest_attacks():
    print("\nDemonstrations d'attaques REST...")
    print("-" * 60)
    subprocess.run([sys.executable, "attacks/attaques_rest.py"])
    input("\nAppuyez sur Entree pour continuer...")

def run_soap_attacks():
    print("\nDemonstrations d'attaques SOAP...")
    print("-" * 60)
    subprocess.run([sys.executable, "attacks/attaques_soap.py"])
    input("\nAppuyez sur Entree pour continuer...")

def show_info():
    clear_screen()
    print("\n" + "=" * 60)
    print("INFORMATIONS DU PROJET")
    print("=" * 60)
    print("\nFichiers du projet:")
    print("  - models.py : Classes Etudiant et GestionEtudiants")
    print("  - etudiants.json : Base de donnees JSON")
    print("  - rest/api_rest.py : Serveur REST (Flask)")
    print("  - rest/client_rest.py : Client de test REST")
    print("  - soap/api_soap.py : Serveur SOAP (Spyne)")
    print("  - soap/client_soap.py : Client de test SOAP")
    print("  - attacks/attaques_rest.py : Attaques REST")
    print("  - attacks/attaques_soap.py : Attaques SOAP")
    print("\nPorts utilises:")
    print("  - REST: 5000")
    print("  - SOAP: 8000")
    print("\nAuthentification REST:")
    print("  - admin / password123")
    print("  - user / user123")
    print("\nEtudiants de test:")
    print("  - ID 1: Diop Amadou (Informatique)")
    print("  - ID 2: Ndiaye Fatou (Mathematiques)")
    print("  - ID 3: Sall Moussa (Physique)")
    print("\n" + "=" * 60)
    input("\nAppuyez sur Entree pour continuer...")

def main():
    while True:
        clear_screen()
        print_menu()
        
        choice = input("Votre choix: ").strip()
        
        if choice == '1':
            start_rest_server()
        elif choice == '2':
            start_soap_server()
        elif choice == '3':
            test_rest_client()
        elif choice == '4':
            test_soap_client()
        elif choice == '5':
            run_rest_attacks()
        elif choice == '6':
            run_soap_attacks()
        elif choice == '7':
            show_info()
        elif choice == '0':
            print("\nAu revoir!")
            break
        else:
            print("\nChoix invalide. Reessayez.")
            input("Appuyez sur Entree pour continuer...")

if __name__ == '__main__':
    main()
