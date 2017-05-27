import collections

class EnsembleRappelle():

    def __init__(self):
        self.ensemble_rappelles = []

    def ajouter(self, rappele):
        self.ensemble_rappelles.append(rappele)

    def __call__(self, *args, **kwargs):
        for rappele in self.ensemble_rappelles:
            rappele(*args, **kwargs)

class KeyPairDict(collections.UserDict):

    #On évite de prendre trop de place en ne gardant que une pair
    #et non une pair et sa transposée car les dictionnaires peuvent
    #rapidement prendre de la place

    def transpose(self, pair):
        element1, element2 = pair
        return element2, element1

    def __contains__(self, key):
        return key in self.data or self.transpose(key) in self.data

    def __setitem__(self, key, value):
        if self.transpose(key) in self.data:
            return self.__setitem__(self.transpose(key), value)
        self.data[key] = value

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        elif self.transpose(key) in self.data:
            return self.data[self.transpose(key)]
        raise KeyError()

    def __delitem__(self, key):
        if key in self.data:
            del self.data[key]
        elif self.transpose(key) in self.data:
            del self.data[self.transpose(key)]
        raise KeyError()

