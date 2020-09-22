from utils import *
from routeutils import *

def transition(x_init,y_init,dir_init,turn_direction,r,alpha,reverse=None, n=None):

    # draw eular spiral if spiral starts at radius at infinity and ends at
    # radius 'r' if reverse=false and vice versa
    diff=0

    Rx=[[cos(dir_init + diff),-sin(dir_init + diff)]]
    Ry=[[sin(dir_init + diff),cos(dir_init + diff)]]

    L=2*r*alpha

    # step=L / (n - 1)
    step=Decimal(GPS_POINT_DISTANCE)
    rem = L % step
    if rem>=(step/2):
        n=L // step
        n+=1
        step=L / n

    s=rangeI(0, L, step)

    fx=lambda v: (v-((v ** 5) / (40 * (r ** 2) * (L ** 2))))
    fy = lambda v: ((v ** 3) / (6*r*L) - ((v ** 7) / (336*(r ** 3)*(L ** 3))))
    x=apply(s, fx)
    y=apply(s, fy)
    negFunc=lambda v: -v

    if turn_direction == 1:
        # turn the transition to the right
        y=apply(y, negFunc)


    if reverse:
        # draw eular spiral if spiral starts at radius 'r' and ends at infinity
        x = apply(x, negFunc)
        xdiff = x[-1] - x[0]
        f1=lambda v: (v - xdiff)
        x=apply(x, f1)

        ydiff = y[-1] - y[0]
        f2=lambda v: (v - ydiff)
        y=apply(y, f2)

        x.reverse()
        y.reverse()

    t=4
    t=0
    h=x[-1 - t] - (r * sin(alpha))
    k=y[-1 - t] + (r * cos(alpha))
    if turn_direction == 1:
        h=x[-1 - t] - (r * sin(alpha))
        k=y[-1 - t] - (r * cos(alpha))

    f1=lambda v: (x_init + v)
    f2=lambda v: (y_init + v)
    coord=[x, y]
    x=apply(matMul(Rx, coord), f1)[0]
    y=apply(matMul(Ry, coord), f2)[0]

    coord=[[h], [k]]
    h = apply(matMul(Rx, coord), f1)[0][0]
    k = apply(matMul(Ry, coord), f2)[0][0]
    return [x,y,h,k]
    
