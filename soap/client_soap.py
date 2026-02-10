from zeep import Client

def main():
    print("TEST DU CLIENT SOAP")
    print("=" * 50)
    
    wsdl = 'http://localhost:8000/?wsdl'
    client = Client(wsdl)
    
    print("\n1. Lister tous les etudiants:")
    result = client.service.lister_etudiants()
    print(f"  {result}")
    
    print("\n2. Obtenir l'etudiant ID 1:")
    result = client.service.obtenir_etudiant(1)
    print(f"  {result}")
    
    print("\n3. Rechercher par filiere (Informatique):")
    result = client.service.rechercher_par_filiere("Informatique")
    print(f"  {result}")
    
    print("\n4. Ajouter un etudiant:")
    result = client.service.ajouter_etudiant(20, "Sarr", "Awa", "Electronique")
    print(f"  {result}")
    
    print("\n5. Modifier l'etudiant ID 20:")
    result = client.service.modifier_etudiant(20, "Sarr", "Awa", "Mecanique")
    print(f"  {result}")
    
    print("\n6. Supprimer l'etudiant ID 20:")
    result = client.service.supprimer_etudiant(20)
    print(f"  {result}")
    
    print("\n" + "=" * 50)
    print("TESTS TERMINES")


if __name__ == '__main__':
    main()
