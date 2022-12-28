from utils import *

# https://hal.archives-ouvertes.fr/hal-00621253/document


class Orderbook:

    def __init__(self, K: int, tick: float, P0: float, a_inf: float = 100, b_inf: float = 100) -> None:
        self.K = K
        self.tick = tick
        self.P = tick*(round(P0/tick))
        self.a_inf = a_inf
        self.b_inf = b_inf

        # On commence avec un carnet d'ordre vide
        self.A = [1 for i in range(K)]
        self.B = [1 for i in range(K)]
        self.Pa = P0+1*tick
        self.Pb = P0-1*tick

    def __repr__(self) -> str:
        return str(self.B)+'\n' + str(self.A)

    def _updatePrice(self) -> None:
        self.Pa = self.tick * round(self.Pa/self.tick)
        self.Pb = self.tick * round(self.Pb/self.tick)
        self.P = (self.Pa+self.Pb)/2

    def _slideAsk(self) -> None:
        ib = minPositiveIndex(self.B)
        ia = minPositiveIndex(self.A)
        deltai = ib-ia
        if deltai > 0:
            self.A = shiftRight(self.A, deltai)
        if deltai < 0:
            self.A = shiftLeft(self.A, -deltai, self.a_inf)

    def _slideBid(self) -> None:
        ib = minPositiveIndex(self.B)
        ia = minPositiveIndex(self.A)
        deltai = ia-ib
        if deltai > 0:
            self.B = shiftRight(self.B, deltai)
        if deltai < 0:
            self.B = shiftLeft(self.B, -deltai, self.b_inf)

    def addLimitAskOrder(self, index: int, q: float) -> None:
        i1 = minPositiveIndex(self.A)
        self.A[index] += q
        i2 = minPositiveIndex(self.A)
        self._slideBid()
        self.Pa -= self.tick*(i1-i2)
        self._updatePrice()

    def addLimitBidOrder(self, index: int, q: float) -> None:
        i1 = minPositiveIndex(self.B)
        self.B[index] += q
        i2 = minPositiveIndex(self.B)
        self._slideAsk()
        self.Pb += self.tick*(i1-i2)
        self._updatePrice()

    def cancelLimitAskOrder(self, index: int, q: float) -> None:
        i1 = minPositiveIndex(self.A)
        self.A[index] = max(0, self.A[index] - q)
        i2 = minPositiveIndex(self.A)
        self._slideBid()
        self.Pa -= self.tick*(i1-i2)
        self._updatePrice()

    def cancelLimitBidOrder(self, index: int, q: float) -> None:
        i1 = minPositiveIndex(self.B)
        self.B[index] = max(0, self.B[index]-q)
        i2 = minPositiveIndex(self.B)
        self._slideAsk()
        self.Pb += self.tick*(i1-i2)
        self._updatePrice()

    def buyMarketOrder(self, q: float) -> float:
        q0 = q
        i = 0
        i1 = minPositiveIndex(self.A)
        moneySpent = 0
        while q0 > 0 and i < self.K:
            temp = self.A[i]
            qTemp = max(0, self.A[i]-q0)
            moneySpent += (self.P+self.tick*(i+0.5))*(temp-qTemp)
            self.A[i] = qTemp
            q0 -= temp
            i += 1
        if q0 > 0 and i == self.K:
            moneySpent += q0*(self.P+(self.K+0.5)*self.tick)
        i2 = minPositiveIndex(self.A)
        self._slideBid()
        self.Pa -= self.tick*(i1-i2)
        self._updatePrice()
        return moneySpent

    def sellMarketOrder(self, q: float) -> float:
        q0 = q
        i = 0
        moneySpent = 0
        i1 = minPositiveIndex(self.B)
        while q0 > 0 and i < len(self.B):
            temp = self.B[i]
            qTemp = max(0, self.B[i]-q0)
            moneySpent += (self.P-self.tick*(i+0.5))*(temp-qTemp)
            self.B[i] = qTemp
            q0 -= temp
            i += 1
        if q0 > 0 and i == len(self.B) - 1:
            moneySpent += q0*(self.P-(self.K+0.5)*self.tick)
        i2 = minPositiveIndex(self.B)
        self._slideAsk()
        self.Pb += self.tick*(i1-i2)
        self._updatePrice()
        return moneySpent

    def getPrice(self) -> [float, float, float]:
        self._updatePrice()
        return (self.Pb, self.Pa, self.P)

    def getBidAskQuantities(self) -> [float, float]:
        return (self.B, self.A)
