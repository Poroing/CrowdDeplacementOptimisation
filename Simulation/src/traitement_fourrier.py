
from math import *
import cmath

##

def doubler_points(signal):
    sortie = [signal[0]]
    for k in range (1,len(signal)):
        sortie.append((signal[k] + signal[k-1])/2)
        sortie.append(signal[k])
    return sortie
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

def signal_mod(signal):
    sortie = []
    
    for z in signal :
        
        sortie.append(abs(z))
        
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
    
    for harmonique in range (n-ordre, n):
        
        sortie[harmonique] = 0
        
    return sortie
    
##

data = recuperation.temps_de_sortie

for _ in range (4):
    data = doubler_points(data)
    print(len(data))





##

#on transforme les signaux temporels en signaux fréquenciels



signal_exp_freq = transfFourrier(data)



##

#on applique le passe bas sur les signaux fréquenciels

result_fourrier_reel1 = passe_bas(signal_exp_freq,0)
result_fourrier_reel2 = passe_bas(signal_exp_freq, 10)
result_fourrier_reel3 = passe_bas(signal_exp_freq, 15)


##

#on effectue la transformée inverse (fréquentiel --> temporel) et on prend la partie réelle du signal

signal_traite_reel1 = signal_mod(transfFourrierInverse(result_fourrier_reel1))
signal_traite_reel2 = signal_mod(transfFourrierInverse(result_fourrier_reel2))
signal_traite_reel3 = signal_mod(transfFourrierInverse(result_fourrier_reel3))

##

plt.plot([0] + signal_traite_reel1, list(range(len(signal_traite_reel1)+1)), 'green')

plt.plot([0] + signal_traite_reel2, list(range(len(signal_traite_reel2)+1)), 'black')

plt.plot([0] + signal_traite_reel3, list(range(len(signal_traite_reel3)+1)), 'pink')

##

plt.plot([0] + data, list(range(len(data)+1)))
plt.show()