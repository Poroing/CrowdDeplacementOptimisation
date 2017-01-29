import traitement_propre 

deriv4 = TraitementDeDonnees(data).debit_ordre_quatre()
deriv1 = TraitementDeDonnees(recuperation.temps_de_sortie).debit_ordre_premier()


temps = [0] +  recuperation.temps_de_sortie


plt.plot(temps, deriv1, 'orange')
plt.plot(list(range(len(data)+1)),deriv4, 'green')

