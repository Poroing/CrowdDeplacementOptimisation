import json


def convertirJsonPython (fichierConfiguration):
    
    donnees_json = open(fichierConfiguration).read()
    
    donnees = json.loads(donnees_json)
    
    return donnees
