from utils import *
from routeutils import *

def circle(x,y,dir_init,turn_direction,r,startAngle=None,endAngle=None):
    # if turn_direction == 1:
    #     th=rangeI(startAngle + dir_init,endAngle + dir_init,- PI / 50)
    # else:
    #     th=rangeI(startAngle + dir_init,endAngle + dir_init, PI / 50)
    # f1 = lambda v: (r * cos(v) ) + x
    # f2 = lambda v: (r * sin(v)) + y
    # xunit = apply(th, f1)
    # yunit = apply(th, f2)
    # return [xunit, yunit]

    angle=endAngle-startAngle
    angleStep=Decimal(GPS_POINT_DISTANCE / r)
    rem = angle % angleStep
    if rem>=(angleStep/2):
        n=angle // angleStep
        n+=1
        angleStep=angle / n
    if turn_direction == 1:
        th=rangeI(startAngle + dir_init,endAngle + dir_init,-angleStep)
    else:
        th=rangeI(startAngle + dir_init,endAngle + dir_init, angleStep)
    f1 = lambda v: (r * cos(v) ) + x
    f2 = lambda v: (r * sin(v)) + y
    xunit = apply(th, f1)
    yunit = apply(th, f2)
    return [xunit, yunit]