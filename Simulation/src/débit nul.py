deriv4 = TraitementDeDonnees(recuperation.temps_de_sortie).debit_ordre_quatre()
deriv1 = TraitementDeDonnees(recuperation.temps_de_sortie).debit_ordre_premier()


temps = [0] +  recuperation.temps_de_sortie


plt.plot(temps, deriv1)
plt.plot(temps,deriv4)
'''
   12 23 43 45 56   
'''