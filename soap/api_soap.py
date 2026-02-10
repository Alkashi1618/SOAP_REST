from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import GestionEtudiants, Etudiant

gestion = GestionEtudiants()


class EtudiantService(ServiceBase):
    
    @rpc(Integer, _returns=Unicode)
    def obtenir_etudiant(ctx, id):
        etudiant = gestion.obtenir_etudiant(id)
        if etudiant:
            return f"ID: {etudiant.id}, Nom: {etudiant.nom}, Prenom: {etudiant.prenom}, Filiere: {etudiant.filiere}"
        return "Etudiant non trouve"
    
    @rpc(_returns=Unicode)
    def lister_etudiants(ctx):
        etudiants = gestion.lister_tous()
        result = []
        for e in etudiants:
            result.append(f"ID: {e.id}, Nom: {e.nom}, Prenom: {e.prenom}, Filiere: {e.filiere}")
        return " | ".join(result)
    
    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def ajouter_etudiant(ctx, id, nom, prenom, filiere):
        etudiant = Etudiant(id, nom, prenom, filiere)
        if gestion.ajouter(etudiant):
            return f"Etudiant {nom} {prenom} ajoute avec succes"
        return "Erreur: Etudiant existe deja"
    
    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def modifier_etudiant(ctx, id, nom, prenom, filiere):
        if gestion.modifier(id, nom, prenom, filiere):
            return f"Etudiant ID {id} modifie avec succes"
        return "Erreur: Etudiant non trouve"
    
    @rpc(Integer, _returns=Unicode)
    def supprimer_etudiant(ctx, id):
        if gestion.supprimer(id):
            return f"Etudiant ID {id} supprime avec succes"
        return "Erreur: Etudiant non trouve"
    
    @rpc(Unicode, _returns=Unicode)
    def rechercher_par_filiere(ctx, filiere):
        etudiants = gestion.rechercher_par_filiere(filiere)
        if etudiants:
            result = []
            for e in etudiants:
                result.append(f"ID: {e.id}, Nom: {e.nom}, Prenom: {e.prenom}")
            return " | ".join(result)
        return "Aucun etudiant trouve dans cette filiere"
    
    @rpc(Unicode, _returns=Unicode)
    def vulnerable_method(ctx, xml_input):
        return f"Traitement de: {xml_input}"


application = Application(
    [EtudiantService],
    tns='gestion.etudiants.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)


if __name__ == '__main__':
    print("Demarrage du serveur SOAP sur http://localhost:8000")
    print("WSDL disponible a: http://localhost:8000/?wsdl")
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
