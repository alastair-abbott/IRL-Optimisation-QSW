from game import Game
from hierarchie import Hierarchie
import cvxpy as cp

operatorsP1 = [0, 1, 2]
operatorsP2 = [0, 3, 4]
operatorsP3 = [0, 5, 6]
operatorsP4 = [0, 7, 8]
operatorsP5 = [0, 9, 10]

P3 = [operatorsP1, operatorsP2, operatorsP3]
P5 = [operatorsP1, operatorsP2, operatorsP3, operatorsP4, operatorsP5]

nbPlayers = 5

v0 = cp.Parameter()
v1 = cp.Parameter()

game = Game(nbPlayers, v0, v1, sym=True) #To solve the 5 player version, change nbPlayers and P3 to P5

prob = Hierarchie(game, P5)
prob.setNashEqConstraints()
v0.value = 0.5
v1.value = 2-v0.value
qsw = prob.optimize(verbose=True, warmStart=False, solver="MOSEK")
print("QSW = {}".format(qsw))


