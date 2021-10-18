import copy
import itertools
from itertools import groupby

def opToPlayer(op, operatorsPlayers):
    """
    Return the player Id with which the operator is associated.
    """
    assert(op != 0) #Id operator associated to every player.
    return (op - 1) // 2

def simplify(monome, playersOperators, monomeSize=None):
    if monomeSize == None:
        monomeSize = len(monome)

    canonic = []

    operators = filter(lambda op: op != 0, monome)  # filter out identity
    operators = sorted(operators, key=lambda op: opToPlayer(op,
                                                            playersOperators))  # Sort without commuting operators of a same player

    for k, g in groupby(operators):
        # GroupBy because the operators are projectors, so op^2 = op
        # if k so that 0 (which correspond to the Id operator) are ignore we put them at the end.
        if k: canonic.append(k)

    # Fill the end with 0 (Id operators)
    while len(canonic) < monomeSize:
        canonic.append(0)

    return canonic

class CanonicMonome:

    def __init__(self, monomeList, i, j, playersOperators):
        """
        create the proba/variable <phi| Si^Dagger Sj |phi>
        """

        #We swap i and j if needed because the matrix is suppose to be symetric.
        if i <= j:
         self.op_i = list(reversed(monomeList[i]))
         self.op_j = monomeList[j]
         self.value = self.op_i + self.op_j
        else:
         self.op_i = list(reversed(monomeList[j]))
         self.op_j = monomeList[i]
         self.value = self.op_i + self.op_j

        self.playersOperators = playersOperators #Operators associated to each player
        self.canonic = self.canonicForm()

    def canonicForm(self):
        return min(simplify(self.value, self.playersOperators), simplify(list(reversed(self.value)), self.playersOperators))

    def __eq__(self, other):
        if not isinstance(other, CanonicMonome):
            return False

        #Two operator are equal if they have the same canonic form.
        return other.canonic == self.canonic

    def __hash__(self):
        return tuple(self.canonic).__hash__()