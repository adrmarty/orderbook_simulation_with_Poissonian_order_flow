"""
minPositiveIndex prend en entrée une liste de nombres lst et 
retourne le plus petit indice i tel que lst[i] est non nul. 
Si i n'existe pas, la fonction retourne la longueur de la liste.
"""


def minPositiveIndex(lst: list[float]) -> int:
    for i in range(len(lst)):
        if lst[i] != 0:
            return i
    return len(lst)


"""
Permet de décaler une liste vers la droite en rajoutant des 0
shiftRight([1, 2, 3, 4], 2) -> [0, 0, 1, 2]
"""


def shiftRight(lst: list[float], k: int) -> list[float]:
    temp = [0 for i in range(k)]+lst
    return temp[:len(lst)]


"""
Permet de décaler une liste vers la gauche en rajoutant des nombres par la droite
shiftLeft([1, 2, 3, 4], 2, 5) -> [3, 4, 5, 5]
"""


def shiftLeft(lst: list[float], k: int, filler: float) -> list[float]:
    temp = lst[k:]+[filler for i in range(k)]
    return temp[:len(lst)]


"""
Permet de tester si une liste contient que des 0 ou non
isEmpty([0, 0, 0, 0]) -> True
"""


def isEmpty(lst: list[float]) -> bool:
    for q in lst:
        if q != 0:
            return False
    return True
