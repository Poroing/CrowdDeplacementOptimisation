from traitement_propre import TraitementDeDonnees

data = recuperation.temps_de_sortie
deriv4 = TraitementDeDonnees(data).debit_ordre_quatre()
deriv1 = TraitementDeDonnees(data).debit_ordre_premier()

deb = TraitementDeDonnees(data).debit_approximatif()
        
plt.plot([0]+data, list(range(len(recuperation.temps_de_sortie) + 1)), 'blue')
##
plt.plot([0]+data, deriv1, 'black')
##
plt.plot([0]+data, deriv4, 'green')
##
plt.plot(deb[1],deb[0],'pink')
