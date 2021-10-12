
import numpy as np
from scipy.optimize import fmin
from toqito.random import random_unitary
from toqito.state_ops import pure_to_mixed

### Deviated Strategy

def QSW(game, theta):
    '''
    Quantum social welfare of the deviated strategy.
    Calculations made in mathematica.
    '''
    assert(game.nbPlayers == 3 or game.nbPlayers == 5)

    # If cvxpy parameters are used.
    try:
        v0, v1 = game.v0.value, game.v1.value
    except:
        v0, v1 = game.v0, game.v1

    if game.nbPlayers == 3:
        return 1 / 192 * (99 * v0 + 81 * v1 + 32 * (v0 - v1) * np.cos(theta) + 8 * (v0 - v1) * np.cos(
            2 * theta) + 5 * v0 * np.cos(4 * theta) + 7 * v1 * np.cos(4 * theta))

    if game.nbPlayers == 5:
        if not game.sym:
            return 1/6144 * (2874*v0 + 2278*v1 + 1984 * (v0 - v1) * np.cos(theta) -
                    2*(v0 + 249*v1)*np.cos(2 * theta) + 32*v0*np.cos(3 * theta) -
                    32*v1*np.cos(3 * theta) + 200*v0*np.cos(4 * theta) +
                    280*v1*np.cos(4 * theta) + 32*v0*np.cos(5 * theta) -
                    32*v1*np.cos(5 * theta) + 3*v0*np.cos(6 * theta) -
                    13*v1*np.cos(6 * theta) - 2*v0*np.cos(8 * theta) + 2*v1*np.cos(8 * theta) -
                    v0*np.cos(10 * theta) - v1*np.cos(10 * theta))
        else:
            return 1/6144 * (3178*v0 + 1974*v1 +
                    1504*(v0 - v1) * np.cos(theta) + (246*v0 - 746*v1) * np.cos(2 * theta) +
                    16*v0 * np.cos(3 * theta) - 16*v1 * np.cos(3 * theta) +
                    152*v0 * np.cos(4 * theta) + 328*v1 * np.cos(4 * theta) +
                    16*v0 * np.cos(5 * theta) - 16*v1 * np.cos(5 * theta) +
                    11*v0 * np.cos(6 * theta) - 21*v1 * np.cos(6 * theta) -
                    2*v0 * np.cos(8 * theta) + 2*v1 * np.cos(8 * theta) - v0 * np.cos(10 * theta) -
                    v1 * np.cos(10 * theta))

def devStratIsNashEq(game):
    '''
    Return true if the deviated strategy is an equilibrium for a given ratio of v0 / V1.

    Value obtained via mathematica.
    I took them with my cursor on the graph... But the equations are to complicated to copy from mathematica to python.
    Not very rigorous.
    '''
    assert(game.nbPlayers == 3 or game.nbPlayers == 5)

    # If cvxpy parameters are used.
    try:
        v0, v1 = game.v0.value, game.v1.value
    except:
        v0, v1 = game.v0, game.v1

    if game.nbPlayers == 3:
        return v0/v1 >= 0.12

    if game.nbPlayers == 5:
        if game.sym:
            return v0/v1 >= 0.38

        else:
            return v0/v1 >= 0.507


def optimalTheta(game):
    '''
    Return the theta that maximize the deviated strategy for given v0 and v1.
    '''
    assert(game.nbPlayers == 3 or game.nbPlayers == 5)
    theta = fmin(lambda theta: - QSW(game, theta), np.pi/2, disp=False)
    return theta

def devStratPOVMs(theta, nbPlayers):
    """
    POVMs for deviated strategy. Only implemented for 3 players
    """
    assert(nbPlayers == 3)
    psi = np.array([np.cos(theta/2), np.sin(theta/2)])
    POVMs_Dict = {}
    for player in range(nbPlayers):
        POVMs_Dict[str(player) + '00'] = np.array([[1, 0], [0,0]])
        POVMs_Dict[str(player) + '10'] = np.array([[0, 0], [0,1]])
        POVMs_Dict[str(player) + '01'] = np.outer(psi, psi)
        POVMs_Dict[str(player) + '11'] = np.eye(2) - np.outer(psi, psi)
    return POVMs_Dict

def devStratRho(theta, nbPlayers):
    """
    Rho for deviated strategy. Only implemented for 3 players
    """
    assert(nbPlayers == 3)
    state = np.array([np.cos(theta/2)**3, np.cos(theta/2)**2 * np.sin(theta/2),
                              np.cos(theta/2)**2 * np.sin(theta/2), -np.cos(theta/2) * np.sin(theta/2)**2,
                              np.cos(theta/2)**2 * np.sin(theta/2),  -np.cos(theta/2) * np.sin(theta/2)**2,
                              -np.cos(theta / 2) * np.sin(theta / 2) ** 2, -np.sin(theta/2)**3])
    return np.outer(state, state)


### Strategy based on graph state measurements

def graphStateStrategy(game):
    """
    Social welfare of the strategy based on measurements of the graphState.
    """
    v0, v1 = game.v0.value, game.v1.value
    if v1 == 0:
        payoutRatio = np.infty
    else:
        payoutRatio = v0 / v1

    assert(game.nbPlayers == 3 or game.nbPlayers == 5)

    socialWelfare = (game.v0.value + game.v1.value)/2

    if game.nbPlayers == 5:
        if game.sym:
            if payoutRatio >= 1/3 and payoutRatio <= 3:
                return socialWelfare
        else:
            if payoutRatio >= 1/2 and payoutRatio <= 2:
                return socialWelfare
    else:
        return socialWelfare

    return None # If none of the case above is verified, the graph strat strategy is not a correlated equilibrium.


def graphState(nbPlayers):
    """
    Return the density matrix associated to the graphState for 3 or 5 players.
    """
    assert(nbPlayers == 3 or nbPlayers == 5)
    if nbPlayers == 3:
        graphStateVec = 1 / np.sqrt(2**3) * np.array([1, 1, 1, -1, 1, -1, -1, -1])
    elif nbPlayers == 5:
        graphStateVec = 1 / np.sqrt(2**5) * np.array([1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1,
                                                   1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1])
    return np.outer(graphStateVec, graphStateVec)

def graphStatePOVMS(nbPlayers):
    POVMS_Dict = {}
    for id in range(nbPlayers):
        POVMS_Dict[str(id) + "00"] = np.array([[1, 0], [0, 0]])
        POVMS_Dict[str(id) + "10"] = np.array([[0, 0], [0, 1]])
        POVMS_Dict[str(id) + "01"] = np.array([[0.5, 0.5], [0.5, 0.5]])
        POVMS_Dict[str(id) + "11"] = np.array([[0.5, -0.5], [-0.5, 0.5]])
    return POVMS_Dict

### GHZ state

def ghzState(nbPlayers):
    """
    Return the density matrix associated to the ghz for 3 or 5 players.
    """
    assert(nbPlayers == 3 or nbPlayers == 5)
    if nbPlayers == 3:
        ghzVec = 1 / np.sqrt(2) * np.array([1, 0, 0, 0, 0, 0, 0, 1])

    elif nbPlayers == 5:
        ghzVec = 1 / np.sqrt(2) * np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])


    return np.outer(ghzVec, ghzVec)


### Random quantum strat

def genRandomPOVMs(nbJoueurs, dimension = 2):
    '''
    Initialise each player with random POVMs
    '''
    opDict = {}
    for playerId in range(nbJoueurs):
        for type in ["0", "1"]:
            U = random_unitary(dimension)
            for answer in ["0", "1"]:

                if (dimension > 2):
                    print("Mauvaise implémentation de la dimension, cf seesaw - ligne 63")
                    exit(0)

                proj = np.transpose([U[int(answer)]])
                opDict[str(playerId) + answer + type] = pure_to_mixed(proj)

    return opDict

