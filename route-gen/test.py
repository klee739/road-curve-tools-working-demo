from curve import *


#[x, y] = circle(0,0,0,0,10, 0, PI/2)
#[x, y, h, k] = transition(0,0,0,0,100,PI/2,False)
[x, y, c]=generateTurn(100,200, 0, 0, 2000, PI/3);

import matplotlib.pyplot as plt
mpl_fig = plt.figure()

plt.scatter(x, y, alpha=1, s=0.2, c="r")

plt.axis('scaled')
plt.show()