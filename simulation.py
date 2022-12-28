from Orderbook import Orderbook
from utils import *
import numpy as np
from random import choices
import display


def simulate_orderbook(K: int, tick: float, P0: float, a_inf: float, b_inf: float,
                                 lambdaM: float, lambdaL: float, lambdaC: float, muM: float,
                                 sM: float, muL: float, sL: float, muC: float, sC: float, simulated_time: float = 6000,
                                 n: int = 1):

    tmax = simulated_time

    nEvent = [1 for _ in range(n)]
    ob = [Orderbook(K, tick, P0, a_inf, b_inf) for _ in range(n)]
    ttemp = [0.0 for i in range(n)]
    t = [0.0 for _ in range(n)]
    priceRecord = [[P0] for _ in range(n)]
    prices = np.array([] for _ in range(n))
    timeRecord = [[0] for _ in range(n)]

    while min(t) < tmax:
        B, A = [], []

        for i in range(n):
            Bi, Ai = ob[i].getBidAskQuantities()
            B.append(Bi)
            A.append(Ai)

        LAMBDACb = [sum([lambdaC[k] * B[i][k]
                         for k in range(len(lambdaC))]) for i in range(n)]
        LAMBDACa = [sum([lambdaC[k] * A[i][k]
                         for k in range(len(lambdaC))]) for i in range(n)]

        LAMBDAL = sum(lambdaL)
        LAMBDAAB = [2*(lambdaM + LAMBDAL) + LAMBDACa[i] + LAMBDACb[i]
                    for i in range(n)]

        deltaT = np.random.exponential(
            [1/LAMBDAAB[i] for i in range(len(LAMBDAAB))], n)
        qM = np.random.lognormal(mean=muM, sigma=sM, size=n)
        qL = np.random.lognormal(mean=muL, sigma=sL, size=n)
        qC = np.random.lognormal(mean=muC, sigma=sC, size=n)

        events = ["buy market", "sell market", "buy limit",
                  "sell limit", "cancel sell order", "cancel buy order"]
        for i in range(n):
            event = choices(events, weights=[
                            lambdaM, lambdaM, LAMBDAL, LAMBDAL, LAMBDACa[i], LAMBDACb[i]])[0]

            if event == "buy market":
                ob[i].buyMarketOrder(qM[i])
            elif event == "sell market":
                ob[i].sellMarketOrder(qM[i])
            elif event == "buy limit":
                k = choices([j for j in range(K)], weights=lambdaL)[0]
                ob[i].addLimitBidOrder(k, qL[i])
            elif event == "sell limit":
                k = choices([j for j in range(K)], weights=lambdaL)[0]
                ob[i].addLimitAskOrder(k, qL[i])

            elif event == "cancel sell order":
                if not isEmpty(A):
                    k = choices([j for j in range(K)], weights=[lambdaC[k]*A[i][k]
                                for k in range(K)])[0]
                    ob[i].cancelLimitAskOrder(k, qC[i])
            elif event == "cancel buy order":
                if not isEmpty(B):
                    k = choices([j for j in range(K)], weights=[
                                lambdaC[k]*B[i][k] for k in range(K)])[0]
                    ob[i].cancelLimitBidOrder(k, qC[i])

            (_, _, Pi) = ob[i].getPrice()

            # midprice recording over time
            priceRecord[i].append(Pi)  
            timeRecord[i].append(t[i])

        t += deltaT
        ttemp += deltaT

    return timeRecord, priceRecord
