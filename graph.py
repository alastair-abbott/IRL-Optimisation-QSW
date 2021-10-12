import numpy as np
import cvxpy as cp
from game import Game
from hierarchie import Hierarchie
from classicalStrategies import genRhoClassic, classicalStratPOVM, bestClassicalStrategy
from quantumStrategies import graphStatePOVMS, graphState, ghzState, genRandomPOVMs
from seesawUtils import fullSeeSaw, quantumEqCheck, printPOVMS
import matplotlib.pyplot as plt
from toqito.state_metrics import fidelity
import quantumStrategies
import os


def readFile(file):
    '''
    Utility function, to load saved txt file.
    '''
    f = open(file, "r")
    data = []
    for element in f.read().split("\n"):
        try:
            data.append(float(element))
        except:
            if element != "":
                print(element)
                data.append(list(element))
    return data


def graph(nbPlayers, sym, delta=0.01, start=0, end=2, seeSawRepeatLow=10, seeSawRepeatHigh=3, treshold=0.4, dimension=2):

    operatorsP1 = [0, 1, 2]
    operatorsP2 = [0, 3, 4]
    operatorsP3 = [0, 5, 6]
    operatorsP4 = [0, 7, 8]
    operatorsP5 = [0, 9, 10]
    P3 = [operatorsP1, operatorsP2, operatorsP3]
    P5 = [operatorsP1, operatorsP2, operatorsP3, operatorsP4, operatorsP5]
    if nbPlayers == 5: P = P5
    else: P = P3
    points = int(np.round((end-start)/delta)) + 1
    x = np.linspace(start, end, points)

    paramV0 = cp.Parameter()
    v1 = 2 - paramV0

    game = Game(nbPlayers, paramV0, v1, sym)
    prob = Hierarchie(game, P)

    print("GraphState & deviated strat & classical strat")
    QSW_GraphState = []
    SW_classical = []
    # QSW_dev = []
    xGraphState = []
    xClassical = []
    # xDev = []

    for idx, v0 in enumerate(x):
        print("iteration {}".format(idx))
        game.v0.value = v0

        SWGraph = quantumStrategies.graphStateStrategy(game)
        if SWGraph is not None:
            QSW_GraphState.append(SWGraph)
            xGraphState.append(game.v0.value)

        SW_classical.append(bestClassicalStrategy(game))
        print(bestClassicalStrategy(game))
        xClassical.append(game.v0.value)

        # # QSW for deviated strat
        # if quantumStrategies.devStratIsNashEq(game):
        #     dev = quantumStrategies.QSW(game, quantumStrategies.optimalTheta(game))
        #     xDev.append(v0)
        #     QSW_dev.append(dev)

    # try:
    #     QSW_NotNash = readFile('data/{}Players_{}Points_Sym{}_HierarchieNoNash.txt'.format(nbPlayers, points, sym))
    #     print("Chargement hierarchie sans contrainte de Nash")

    # except:
    #     print("Hierarchie Sans contrainte de Nash")
    #     QSW_NotNash = []
    #     for idx, v0 in enumerate(x):
    #         print("iteration {}".format(idx))
    #         paramV0.value = v0
    #         qsw = prob.optimize(verbose=False, warmStart=True, solver="MOSEK")
    #         QSW_NotNash.append(qsw)

    #     with open('data/{}Players_{}Points_Sym{}_HierarchieNoNash.txt'.format(nbPlayers, points, sym), 'w') as f:
    #         for item in QSW_NotNash:
    #             f.write("%s\n" % item)

    try:
        QSW_Nash = readFile('data/{}Players_{}Points_Sym{}_HierarchieNash.txt'.format(nbPlayers, points, sym))
        print("Chargement hierarchie avec contrainte de Nash")

    except:
        print("Hierarchie avec contrainte de Nash")
        QSW_Nash = []

        prob.setNashEqConstraints()

        for idx, v0 in enumerate(x):
            print("iteration {}".format(idx))
            paramV0.value = v0
            qsw = prob.optimize(verbose=False, warmStart=True, solver="MOSEK")
            QSW_Nash.append(qsw)

        with open('data/{}Players_{}Points_Sym{}_HierarchieNash.txt'.format(nbPlayers, points, sym), 'w') as f:
            for item in QSW_Nash:
                f.write("%s\n" % item)

    try:
        QSW_SeeSaw = readFile('data/{}Players_{}Points_Sym{}_SeeSaw.txt'.format(nbPlayers, points, sym))
        Winrate_SeeSaw = readFile('data/{}Players_{}Points_Sym{}_SeeSaw_Winrate.txt'.format(nbPlayers, points, sym))
        print("Chargement SeeSaw")


    except:
        print("SeeSaw")
        graphStateMatrix = graphState(nbPlayers)
        game = Game(nbPlayers, 0, 0, sym)

        lastGraphStateInit = (graphStatePOVMS(nbPlayers), graphStateMatrix)
        lastInit = (graphStatePOVMS(nbPlayers), graphStateMatrix)


        QSW_SeeSaw = []
        Winrate_SeeSaw = []


        #If one of them exist, we remove the file.
        if os.path.exists('data/{}Players_{}Points_Sym{}_SeeSaw.txt'.format(nbPlayers, points, sym)):
            os.remove('data/{}Players_{}Points_Sym{}_SeeSaw.txt'.format(nbPlayers, points, sym))

        if os.path.exists('data/{}Players_{}Points_Sym{}_SeeSaw_Winrate.txt'.format(nbPlayers, points, sym)):
            os.remove('data/{}Players_{}Points_Sym{}_SeeSaw_Winrate.txt'.format(nbPlayers, points, sym))

        prevMax = 1

        for it, v0 in enumerate(reversed(x)):
            game.v0 = v0
            game.v1 = 2 - v0

            print("\nGlobal Iteration {} v0 {}".format(it, v0))
            maxQsw = 0

            nbRepeat = seeSawRepeatLow * (v0 < treshold) + seeSawRepeatHigh * (v0 >= treshold)
            #On pourrait couper si on est proche de la borne de la hierarchie

            for r in range(nbRepeat):
                print("nbRepeat {}".format(r))

                if r == 0:
                    # Following strat with POVMs near graphstate ones
                    qsw, seeSaw = fullSeeSaw(game, dimension=dimension, init=lastGraphStateInit)
                    lastGraphStateInit = (seeSaw.POVM_Dict, seeSaw.genRho())
                if r == 1:
                    #Takes best init for last value of v0
                    qsw, seeSaw = fullSeeSaw(game, dimension=dimension, init=lastInit)

                if r == 2:
                    initClassical = (classicalStratPOVM(game), genRhoClassic(game.nbPlayers))
                    qsw, seeSaw = fullSeeSaw(game, dimension=dimension, init=initClassical)
                    
                else:
                    #Random init
                    init = (seeSaw.genPOVMs(), seeSaw.genRho())
                    qsw, seeSaw = fullSeeSaw(game, dimension=dimension, init=init)

                maxQsw = max(maxQsw, qsw)

                ###UNCOMMENT TO HAVE RANDOM INIT.
                #First repetition take best POVMs for last V0 value. After it takes random POVMs.

                # If it's the best result we encoutered yet for this v0's value, we save the strategy.
                if maxQsw == qsw:
                    bestSeeSaw = seeSaw
                    maxDiff = abs(prevMax - maxQsw)

            # If huge diff, we do another cyle on a strategy which as already been optimized.
            # Otherwise we have "holes" where the qsw collapse when we shift of strategy class
            # (i.e when we go from quantum strat to classicals)
            iter = 0
            while maxDiff >= 0.05 and v0 != 0 and iter <= 1:
                print("another cycle")
#
                #Best of last iteration
                if iter == 0:
                    init = (bestSeeSaw.genPOVMs(), seeSaw.genRho())
                    qsw, seeSaw = fullSeeSaw(game, dimension=dimension, init=init)
#
#                #GraphState povms
                if iter == 1:
                    qsw, seeSaw = fullSeeSaw(game, dimension=dimension, init=lastGraphStateInit)
#
#                else:
#                    init = (seeSaw.genPOVMs(), seeSaw.genRho())
#                    qsw, seeSaw = fullSeeSaw(nbPlayers, v0, v1, init=init,  sym=sym)
#                    init = (seeSaw.POVM_Dict, seeSaw.genRho())
#                    qsw, seeSaw = fullSeeSaw(nbPlayers, v0, v1, init=init,  sym=sym)
#
#
                maxQsw = max(maxQsw, qsw)

                if maxQsw == qsw:
                    bestSeeSaw = seeSaw
                    maxDiff = abs(prevMax - maxQsw)
#
                iter+=1
#
            prevMax = maxQsw
            QSW_SeeSaw.append(maxQsw)
            Winrate_SeeSaw.append(bestSeeSaw.winrate)

            lastInit = (bestSeeSaw.POVM_Dict, seeSaw.genRho()) #If we keep old rho, we often (always ?) stay on the same equilibrium.

            printPOVMS(bestSeeSaw)
            print("Rho:")
            print(bestSeeSaw.rho)
            print("Trace of rho squared:", np.trace(np.dot(bestSeeSaw.rho, bestSeeSaw.rho)))
            print("Fidelity with graphState", fidelity(bestSeeSaw.rho, graphStateMatrix))

        with open('data/{}Players_{}Points_Sym{}_SeeSaw.txt'.format(nbPlayers, points, sym), 'w') as f:
            for item in QSW_SeeSaw:
                f.write("%s\n" % item)

        with open('data/{}Players_{}Points_Sym{}_SeeSaw_Winrate.txt'.format(nbPlayers, points, sym), 'w') as f:
            for item in Winrate_SeeSaw:
                f.write("%s\n" % item)

    fig, axs = plt.subplots(1, constrained_layout = True, figsize=(10, 10))
    fig.suptitle("Graph for {} players with {} points, sym: {}".format(nbPlayers, points, sym))

    axs.plot([v/2 for v in xGraphState], QSW_GraphState, label="GraphState")
    axs.plot(x/2, QSW_Nash, label="HierarchieNash")
    # axs.plot(x/2, QSW_NotNash, label="HierarchieNotNash")
    axs.plot(x/2, list(reversed(QSW_SeeSaw)), label="SeeSaw")
    # axs.plot(x, list(reversed(Winrate_SeeSaw)), label="Winrate Seesaw")
    axs.plot([v/2 for v in xClassical], SW_classical, label="SW best classical strat")
    # axs.plot([v/2 for v in xDev], QSW_dev, label="SW of deviated strat")

    axs.set_title("Quantum social welfare")
    axs.set_xlabel("v0/(v0+v1)")
    axs.set_ylabel("QSW")
    axs.set_ylim([0, 2])
    axs.legend(loc="upper right")

    plt.show()

if __name__ == '__main__':
    nbPlayers = 5
    sym=False #Sym for 5 players
    delta = 0.01
    start = 0
    end = 2
    seeSawRepeatLow = 3
    seeSawRepeatHigh = 3
    treshold = 0.33
    dimension = 2 #Only change dimension used in seeSaw, not on the Hierarchie.

    graph(nbPlayers, sym, delta, start, end, seeSawRepeatLow, seeSawRepeatHigh, treshold, dimension=dimension)


