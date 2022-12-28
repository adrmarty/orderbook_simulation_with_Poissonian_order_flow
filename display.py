import numpy as np
from matplotlib import pyplot as plt
from scipy import stats


def show_price_graph(timeRecord, priceRecord):
    plt.plot(timeRecord, priceRecord)
    plt.annotate("simulated time: " +
                 str(timeRecord[-1])[:10], xy=(0, 1), xycoords='axes fraction')
    plt.show()
