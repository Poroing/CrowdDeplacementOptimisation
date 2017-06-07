import sys
sys.path.append('..')
import threaded_simulations
from convertir_json_python import convertirJsonPython

if __name__ == '__main__':
    configuration = convertirJsonPython(
        '../FichiersConfiguration/MPSTAR.json')

    for debit in threaded_simulations.avoirDebitsMoyenSimulation(
            1000,
            configuration):
        print(debit)
