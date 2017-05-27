import sys
sys.path.append('..')
import multiprocessing
import traitement
import logging
        
def lancer(arguments_recuperations_queue, temps_de_sortie_queue):
    for args_recuperation, kwargs_recuperation in iter(arguments_recuperations_queue.get, 'FIN'):
        recuperation = traitement.RecuperationDeDonnees(
            *args_recuperation,
            **kwargs_recuperation)

        recuperation.lancer()
        temps_de_sortie_queue.put(recuperation.temps_de_sortie)

    temps_de_sortie_queue.put('FIN')

def traiter(
        temps_de_sortie_queue,
        fonction_traitement,
        resultats_queue,
        nombre_traiteur):

    nombre_traieur_ayant_finie = 0
    while nombre_traieur_ayant_finie < nombre_traiteur:
        temps_de_sortie = temps_de_sortie_queue.get()
        if temps_de_sortie == 'FIN':
            nombre_traieur_ayant_finie += 1
        else:
            resultats_queue.put(fonction_traitement(temps_de_sortie))

    resultats_queue.put('FIN')

def avoirDebitMoyen(temps_de_sortie):
    traitement_donnee = traitement.TraitementDeDonnees(temps_de_sortie)
    return traitement_donnee.avoirDebitMoyen()

def avoirDebitsMoyenSimulation(
        nombre_simulation,
        configuration,
        arreter_apres_temps=True,
        temps=15,
        arreter_apres_sortie=True,
        nombre_coeur=4):

    arguments_recuperations_queue = multiprocessing.Queue()
    temps_de_sortie_queue = multiprocessing.Queue()
    resultats_queue = multiprocessing.Queue()

    for _ in range(nombre_simulation):
        arguments_recuperations_queue.put((
            [configuration],
            dict(
                arreter_apres_temps=arreter_apres_temps,
                temps_maximal=temps,
                arreter_apres_sortie=arreter_apres_sortie)))

    for _ in range(nombre_coeur):
        arguments_recuperations_queue.put('FIN')

    lanceurs = []
    for _ in range(nombre_coeur):
        lanceurs.append(multiprocessing.Process(
            target=lancer,
            args=(
                arguments_recuperations_queue,
                temps_de_sortie_queue)))
        lanceurs[-1].start()

    traiteur = multiprocessing.Process(
        target=traiter,
        args=(
            temps_de_sortie_queue,
            avoirDebitMoyen,
            resultats_queue,
            nombre_coeur))
    traiteur.start()

    return iter(resultats_queue.get, 'FIN')
