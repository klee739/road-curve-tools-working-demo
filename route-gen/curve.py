from transition import *
from circle import *
from curvemodel import *

def generateTurn(x_init,y_init,dir_init,turn_direction,r,angle):
    gtcurve = GroundTruthCurve(-1, None, None, None)
    gtcurve.transitionPC = GPS(x_init, y_init)

    #right now we define the transition section as 1/8 of the angle
    pc_angle=angle / 4
    pt_angle=pc_angle
    curve_angle=angle - (pc_angle + pt_angle)
    [x,y,h,k]=transition(x_init,y_init,dir_init,turn_direction,r,pc_angle,False)

    gtcurve.pc = GPS(x[-1], y[-1])
    gtcurve.center = GPS(h, k)

    gtcurve.type = CurveType.SIMPLE

    if turn_direction == 1:
        [xp,yp]=circle(h,k,dir_init- pc_angle,turn_direction,r,PI / 2,PI / 2  - curve_angle)
    else:
        [xp,yp]=circle(h,k,dir_init+ pc_angle,turn_direction,r,- PI / 2,-PI / 2 + curve_angle)
    x=x+xp
    y=y+yp
    gtcurve.pt = GPS(x[-1], y[-1])
    diff=0
    if turn_direction == 1:
        diff=-2*angle

    [xp,yp,_,_]=transition(xp[-1],yp[-1],dir_init + angle + diff,turn_direction,r,pt_angle,True)
    x=x+xp
    y=y+yp
    gtcurve.transitionPT = GPS(x[-1], y[-1])

    return [x, y, gtcurve]
