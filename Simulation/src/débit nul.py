import traitement_propre 


data = recuperation.temps_de_sortie
deriv4 = TraitementDeDonnees(data).debit_ordre_quatre()
deriv1 = TraitementDeDonnees(recuperation.temps_de_sortie).debit_ordre_premier()


        
plt.plot(temps, list(range(len(recuperation.temps_de_sortie) + 1)), 'blue')
plt.plot(temps, deriv1, 'orange')
plt.plot(temps, deriv4, 'green')

