X = [0] + recuperation.temps_de_sortie

Y = list(range(len(recuperation.temps_de_sortie) + 1))


def polLagrange(X, j, a):
    
    coef = 1
        
    for i in range (0,j): #produit pour i < j
            
        coef *= (a-X[i])/(X[j]-X[i])
        
    for i in range(j+1, len(X)): #produit pour i > j
        
        coef *= (a-X[i])/(X[j]-X[i])
        
    return coef

def interpolation(X,Y,a):
    
    coef = 0
    
    for j in range (0, len(Y)): #on interpolle à l'aide des polynômes de Lagrange
        
        coef += Y[j] * polLagrange(X,j,a)
        
    return coef
    
    
    
abs = [k/100 for k in range (600,900)]

##

def interval(X,Y,a):
    ind = 0
    while X[ind]<a :
        ind+=1
        
    ind = ind//10
    
    return [X[k] for k in range (ind*10,(ind+1)*10)],[Y[k] for k in range (ind*10,(ind+1)*10)]
##
def interpolation_par_parties(X,Y,a):
    
    return (interpolation(interval(X,Y,a)[0],interval(X,Y,a)[1],a))
##

plot(abs,[interpolation_par_parties(X,Y,a) for a in abs])

plot(X,Y,'green')