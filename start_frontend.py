#!/usr/bin/env python3
"""
Lanceur automatique pour le frontend
Lance le serveur REST puis ouvre le frontend dans le navigateur
"""
import subprocess
import webbrowser
import time
import sys
import os


def print_banner():
    print("=" * 60)
    print("    LANCEMENT DE L'INTERFACE WEB")
    print("=" * 60)
    print()


def start_rest_server():
    """Démarrer le serveur REST"""
    print("Démarrage du serveur REST...")
    print("   URL: http://127.0.0.1:5050")
    print()

    # Changer de répertoire vers la racine du projet
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # Lancer le serveur REST en arrière-plan
    try:
        if sys.platform == 'win32':
            # Windows
            server_process = subprocess.Popen(
                [sys.executable, "rest/api_rest.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac
            server_process = subprocess.Popen(
                [sys.executable, "rest/api_rest.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        print(" Serveur REST démarré")
        return server_process
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur: {e}")
        return None


def open_frontend():
    """Ouvrir le frontend dans le navigateur"""
    print("\nOuverture de l'interface web...")

    # Attendre que le serveur soit prêt
    time.sleep(2)

    # Chemin vers index.html
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "index.html")
    frontend_url = f"file:///{os.path.abspath(frontend_path).replace(os.sep, '/')}"

    # Ouvrir dans le navigateur par défaut
    webbrowser.open(frontend_url)

    print("Interface web ouverte dans le navigateur")
    print()


def main():
    print_banner()

    # Démarrer le serveur REST
    server_process = start_rest_server()

    if server_process is None:
        print("\nImpossible de démarrer. Vérifiez que Python et les dépendances sont installés.")
        return

    # Ouvrir le frontend
    open_frontend()

    print("=" * 60)
    print("TOUT EST PRÊT !")
    print("=" * 60)
    print("\nINSTRUCTIONS:")
    print("  1. L'interface web est ouverte dans votre navigateur")
    print("  2. Le serveur REST tourne sur http://127.0.0.1:5050")
    print("  3. Appuyez sur Ctrl+C pour arrêter")
    print()
    print("AUTHENTIFICATION:")
    print("  - Username: admin")
    print("  - Password: password123")
    print()
    print("=" * 60)

    try:
        # Garder le script en vie
        print("\nServeur en cours d'exécution... Appuyez sur Ctrl+C pour arrêter\n")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\n Arrêt du serveur...")
        server_process.terminate()
        server_process.wait()
        print(" Serveur arrêté. Au revoir !")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n ERREUR: {e}")
        print("\nConsultez README.md pour l'aide")
        sys.exit(1)