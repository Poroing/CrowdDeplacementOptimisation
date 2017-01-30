import math

def avoirPolynomeLagrange(X, j):
    def polynome(x):
        valeur = 1
        for i in range (0, len(X)):
            if i == j: continue
            valeur *= (x - X[i])/(X[j] - X[i])
        return valeur
    return polynome

def avoirPolynomeInterpolateurLagrange(X, Y):
    polynomes_lagrange = [ avoirPolynomeLagrange(X, i) for i in range(len(X)) ]
    def polynome_interpolateur(x):
        valeur = 0
        for j in range (0, len(Y)): #on interpolle à l'aide des polynômes de Lagrange
            valeur += Y[j] * polynomes_lagrange[j](x)
        return valeur
    return polynome_interpolateur

def enleverValeursProches(X, Y, epsilon):
    sortie_X = [ X[0] ]
    sortie_Y = [ Y[0] ]
    for x, y in zip(X, Y):
        if math.isclose(x, sortie_X[-1], abs_tol=epsilon):
            continue
        sortie_X.append(x)
        sortie_Y.append(y)
    return sortie_X, sortie_Y

def decouperIntervalleAvecPointCommunAuExtremite(X, Y, points_par_intervalle):
    sortie = [([], [])]
    for x, y in zip(X, Y):
        if len(sortie[-1][0]) >= points_par_intervalle:
            sortie[-1][0].append(x)
            sortie[-1][1].append(y)
            sortie.append(([], []))
        sortie[-1][0].append(x)
        sortie[-1][1].append(y)
    return sortie

def indexIntervalle(bornes, x):
    a, b = 0, len(bornes) - 1
    while a != b:
        milieu = (a + b) // 2
        if x < bornes[milieu]:
            b = milieu - 1
        elif x > bornes[milieu + 1]:
            a = milieu + 1
        else:
            return milieu
    return a
    

def avoirFonctionInterpolatriceParIntervalle(X, Y, points_par_intervalle):
    decoupage = decouperIntervalleAvecPointCommunAuExtremite(X, Y, points_par_intervalle)
    polynomes = [ avoirPolynomeInterpolateurLagrange(sous_X, sous_Y)
        for sous_X, sous_Y in decoupage ]
    bornes = list(map(lambda abscisse_ordonee: abscisse_ordonee[0][0], decoupage))
    def fonction(x):
        index = indexIntervalle(bornes, x)
        return polynomes[indexIntervalle(bornes, x)](x)
    return fonction
    
def interval(X,Y,a):
    ind = 0
    while X[ind]<a :
        ind+=1
    ind = ind//10
    
    return [X[k] for k in range (ind*10,(ind+1)*10)],[Y[k] for k in range (ind*10,(ind+1)*10)]

def interpolation_par_parties(X,Y,a):
    return (interpolation(interval(X,Y,a)[0],interval(X,Y,a)[1],a))


