import json


def convertir_Json_python (fichierConfiguration):
    
    donnees_json = open(fichierConfiguration).read()
    
    donnees = json.loads(donnees_json)
    
    return donnees