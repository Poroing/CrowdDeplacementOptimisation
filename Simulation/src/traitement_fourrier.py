recuperation.temps_de_sortie

##
def transfFourrier(signalTemp):
    signalFreq = []
    N = len(signalTemp)
    for k in range(N-1):
        coef = 0
        for i in range(N-1):
            coef += signalTemp[i]*(complex(cos(-2*pi*k*i/N),sin(-2*pi*k*i/N)))
        signalFreq.append(coef)
    return signalFreq
    

##
def signal_reel(signal):
    sortie = []
    for x in signal :
        sortie.append(x.real)
    return sortie
    
##
def module_signal(signal_complexe):
    sortie = []
    for x in signal_complexe :
        sortie.append(phase(x))
    return sortie
##

def transfFourrierInverse(signalFreq):
    signalTemp = []
    N = len(signalFreq)
    for n in range(N-1):
        coef = 0
        for k in range(N-1):
            coef += signalFreq[k]*complex(cos(2*pi*n*k*(1/N)),sin(2*pi*n*k*(1/N)))
        signalTemp.append(coef*(1/N))
    return signalTemp
    
##

def passe_bas(signalFreq, ordre):
    n = len(signalFreq)-1
    sortie = [x for x in signalFreq]
    for harmonique in range (ordre, n):
        sortie[harmonique] = 0
    return sortie
    

##
signal_exp_freq = transfFourrier(recuperation.temps_de_sortie)

signal_exp_reel = signal_exp_freq

signal_exp_mod = signal_exp_freq

##
result_fourrier_reel1 = passe_bas(signal_exp_reel, 10)
result_fourrier_reel2 = passe_bas(signal_exp_reel, 20)
result_fourrier_reel3 = passe_bas(signal_exp_reel, 30)
result_fourrier_reel4 = passe_bas(signal_exp_reel, 40)




result_fourrier_mod = passe_bas(signal_exp_mod, 25)


##

signal_traite_reel1 = signal_reel(transfFourrierInverse(result_fourrier_reel1))
signal_traite_reel2 = signal_reel(transfFourrierInverse(result_fourrier_reel2))
signal_traite_reel3 = signal_reel(transfFourrierInverse(result_fourrier_reel3))
signal_traite_reel4 = signal_reel(transfFourrierInverse(result_fourrier_reel4))

signal_traite_mod = module_signal(transfFourrierInverse(result_fourrier_mod))
##

plt.plot([0] + signal_traite_reel1, list(range(len(signalLisse)+1)), 'red')

plt.plot([0] + signal_traite_reel2, list(range(len(signalLisse)+1)), 'black')

plt.plot([0] + signal_traite_reel3, list(range(len(signalLisse)+1)), 'green')

plt.plot([0] + signal_traite_reel4, list(range(len(signalLisse)+1)), 'pink')


plt.plot([0] + recuperation.temps_de_sortie, list(range(len(recuperation.temps_de_sortie)+1)))
plt.show()