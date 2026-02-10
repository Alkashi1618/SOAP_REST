import json
import os

class Etudiant:
    def __init__(self, id, nom, prenom, filiere):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.filiere = filiere
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'filiere': self.filiere
        }
    
    @staticmethod
    def from_dict(data):
        return Etudiant(
            data['id'],
            data['nom'],
            data['prenom'],
            data['filiere']
        )


class GestionEtudiants:
    def __init__(self, fichier='etudiants.json'):
        self.fichier = fichier
        self.etudiants = []
        self.charger()
    
    def charger(self):
        if os.path.exists(self.fichier):
            with open(self.fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.etudiants = [Etudiant.from_dict(e) for e in data]
    
    def sauvegarder(self):
        with open(self.fichier, 'w', encoding='utf-8') as f:
            data = [e.to_dict() for e in self.etudiants]
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def ajouter(self, etudiant):
        if self.obtenir_etudiant(etudiant.id):
            return False
        self.etudiants.append(etudiant)
        self.sauvegarder()
        return True
    
    def obtenir_etudiant(self, id):
        for e in self.etudiants:
            if e.id == id:
                return e
        return None
    
    def lister_tous(self):
        return self.etudiants
    
    def modifier(self, id, nom, prenom, filiere):
        etudiant = self.obtenir_etudiant(id)
        if etudiant:
            etudiant.nom = nom
            etudiant.prenom = prenom
            etudiant.filiere = filiere
            self.sauvegarder()
            return True
        return False
    
    def supprimer(self, id):
        etudiant = self.obtenir_etudiant(id)
        if etudiant:
            self.etudiants.remove(etudiant)
            self.sauvegarder()
            return True
        return False
    
    def rechercher_par_filiere(self, filiere):
        return [e for e in self.etudiants if e.filiere.lower() == filiere.lower()]
