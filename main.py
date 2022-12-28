from matplotlib import pyplot as plt
from simulation import simulate_orderbook
import display

import numpy as np
import scipy.stats as stats
import scipy
import time

# https://hal.archives-ouvertes.fr/hal-00621253/document


# ---- model parameters ----

# average price
P0 = 1000
# tick is minimal gap between two prices in the order book
tick = 0.01

# boundaries for the bid and ask sides of the orderbook expressed in volume
a_inf = 250
b_inf = 250


# the prices in the order book go from P -K*tick to P+K*tick
# where P is the actual price of the asset
K = 13

# units of all lambdas is s^-1

# lambdaM is estimated from page 37 of the paper (120)
lambdaM = 5

# lambdaL is estimated from page 37 of the paper (121)
# lambdaL = [1/(i+1)**0.5 for i in range(0, K)]
lambdaL = [0.2842, 0.5255, 0.2971, 0.2307, 0.0826, 0.0682,
           0.0631, 0.0481, 0.0462, 0.0321, 0.0178, 0.0015, 0.0001]

# lambdaC is estimated from page 37 of the paper (122)
lambdaC = [0.8636, 0.4635, 0.1487, 0.1096, 0.0402, 0.0341,
           0.0311, 0.0237, 0.0233, 0.0178, 0.0127, 0.0012, 0.0001]
lambdaC = [lambdaC[i]*10**(-3) for i in range(len(lambdaC))]

# the next paramters are estimated according to page 38


muM = 4
sM = 1.2

muL = 4.5
sL = 0.8

muC = 4.5
sC = 0.8

# ---- simulation ----

t0 = time.time()

(timeRecord, priceRecord) = simulate_orderbook(K, tick, P0, a_inf,
                                                         b_inf, lambdaM, lambdaL, lambdaC, muM, sM, muL, sL, muC, sC, n=1)
print("computation time : ", time.time()-t0, " seconds")


# Display
for i in range(len(timeRecord)):
    display.show_price_graph(timeRecord[i], priceRecord[i])
