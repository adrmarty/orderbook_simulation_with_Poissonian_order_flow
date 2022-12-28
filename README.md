# Orderbook simulation with Poissonian order flow
This python code is an implementation of this paper : [A Mathematical Approach to Order Book Modelling (2013)](https://hal.archives-ouvertes.fr/hal-00621253/document). This paper models a limit order book and allows us to simulate one. This is very useful to backtest HFT strategies or any strategy depending on market microstructures. The parameters of this model have to be estimated from an actual order book, if you want to simulate a given market / pair. This is because all of the microstructure information is captured by the intensities of order arrivals and the density of their quantities according to this model. I highly recommend reading the paper, because the authors explain how to estimate these parameters. You can also read this very interesting paper which explains another (more precise) way to estimate these parameters : [Modelling intensities of order flows in a limit order book (2016)](https://hal-centralesupelec.archives-ouvertes.fr/hal-01705080/file/ModellingIntensities.pdf).

If you have any question feel free to contact me on Twitter @Sabrebar