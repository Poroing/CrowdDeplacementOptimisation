import sys
sys.path.append('..')
import geometrie
import math

print(geometrie.avoirMilieuProche(math.pi, math.pi))
print(geometrie.avoirMilieuProche(3 * math.pi, math.pi))
print(geometrie.avoirMilieuProche(math.pi / 100, 0))
