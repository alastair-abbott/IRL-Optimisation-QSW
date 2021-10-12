import numpy as np


def bestClassicalStrategy(game):
    """
    Social welfare of the best classical strategy for a given game.
    """
    try:
        v0, v1 = game.v0.value, game.v1.value
    except:
        v0, v1 = game.v0, game.v1

    if v1 == 0:
        payoutRatio = np.infty
    else:
        payoutRatio = v0 / v1

    assert(game.nbPlayers == 3 or game.nbPlayers == 5)

    if game.nbPlayers == 5:
        if not game.sym:
            if payoutRatio <= 1 / 3:
                socialWelfare = 1/30 * (8 * v0 + 17 * v1)
            elif payoutRatio <= 1:
                socialWelfare = 1/30 * (6 * v0 + 19 * v1)
            else:
                socialWelfare = 1/30 * 25 * v0
        else:
            if payoutRatio <= 1 / 3:
                socialWelfare = 1 / 30 * (4 * v0 + 11 * v1)
            elif payoutRatio <= 1:
                socialWelfare = 1 / 30 * (5 * v0 + 20 * v1)
            else:
                socialWelfare = 1/30 * 25 * v0
    else:
        if payoutRatio <= 1:
            socialWelfare = 1/12 * (7 * v1 + 2 * v0)
        else:
            socialWelfare = 1/12 * 9 * v0

    return socialWelfare


def genRhoClassic(nbPlayers):
    """
    Simple classical rho.
    """
    n = 2**nbPlayers
    rho = np.zeros((n, n))
    rho[0][0] = 1
    return rho

def classicalStratPOVM(game):
    """
    Generate the POVMs corresponding to the best classical strategy for a given game.
    """
    assert(game.nbPlayers == 5 or game.nbPlayers == 3)
    try:
        v0, v1 = game.v0.value, game.v1.value
    except:
        v0, v1 = game.v0, game.v1

    payoutRatio = v0/v1
    opDict = {}
    if game.nbPlayers == 5:
        if game.sym:
            if payoutRatio <= 1/3:
                #Not Not 1 1 1
                #Two players Not
                for playerId in range(2):
                    opDict[str(playerId) + "00"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "10"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "01"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "11"] = np.array([[0, 0], [0, 0]])

                #Three players 1
                for playerId in range(2, 5):
                    opDict[str(playerId) + "00"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "10"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "01"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "11"] = np.array([[0, 0], [0, 0]])

            elif payoutRatio >= 1 / 3:
                # Id Id 1 1 1
                # Two players Id
                for playerId in range(2):
                    opDict[str(playerId) + "00"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "10"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "01"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "11"] = np.array([[1, 0], [0, 1]])

                # Three players 1
                for playerId in range(2, 5):
                    opDict[str(playerId) + "00"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "10"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "01"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "11"] = np.array([[1, 0], [0, 1]])
        else:
            if payoutRatio <= 1 / 3:
                print("v0/v1 = {} Not Not Not Not 1".format(payoutRatio))
                # Not Not Not Not 1
                for playerId in range(4):
                    opDict[str(playerId) + "00"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "10"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "01"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "11"] = np.array([[0, 0], [0, 0]])

                opDict["4" + "00"] = np.array([[0, 0], [0, 0]])
                opDict["4" + "10"] = np.array([[1, 0], [0, 1]])
                opDict["4" + "01"] = np.array([[1, 0], [0, 1]])
                opDict["4" + "11"] = np.array([[0, 0], [0, 0]])

            elif payoutRatio >= 1 / 3:
                print("v0/v1 = {} Id Id 1 1 1".format(payoutRatio))
                # Id Id 1 1 1
                # Two players Id
                for playerId in range(2):
                    opDict[str(playerId) + "00"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "10"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "01"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "11"] = np.array([[1, 0], [0, 1]])

                # Three players 1
                for playerId in range(2, 5):
                    opDict[str(playerId) + "00"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "10"] = np.array([[1, 0], [0, 1]])
                    opDict[str(playerId) + "01"] = np.array([[0, 0], [0, 0]])
                    opDict[str(playerId) + "11"] = np.array([[1, 0], [0, 1]])

    if game.nbPlayers == 3:
        for playerId in range(2):
            opDict[str(playerId) + "00"] = np.array([[1, 0], [0, 1]])
            opDict[str(playerId) + "10"] = np.array([[0, 0], [0, 0]])
            opDict[str(playerId) + "01"] = np.array([[0, 0], [0, 0]])
            opDict[str(playerId) + "11"] = np.array([[1, 0], [0, 1]])

        # Three players 1
        opDict[str(2) + "00"] = np.array([[0, 0], [0, 0]])
        opDict[str(2) + "10"] = np.array([[1, 0], [0, 1]])
        opDict[str(2) + "01"] = np.array([[0, 0], [0, 0]])
        opDict[str(2) + "11"] = np.array([[1, 0], [0, 1]])

    return opDict
