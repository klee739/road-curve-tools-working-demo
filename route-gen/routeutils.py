
from routemodel import *
from routeconstants import *
from curveutils import *
from decimal import Decimal
import math
import copy
#from curve import *

def sin(angle):
    return Decimal(math.sin(angle))

def cos(angle):
    return Decimal(math.cos(angle))
def normalizeAngle(angle):
    newAngle = angle
    if newAngle >= (2 * PI):
        newAngle -= (2 * PI)
    elif newAngle < 0:
        newAngle += (2 * PI)
    return newAngle

def travelLine(routePosition, roadSectionLine):
    lastRoutePosition=RoutePosition(routePosition.coordinates, routePosition.direction)
    travelLengthLeft = roadSectionLine.length
    gpsPoints=[]
    travelStep = GPS_POINT_DISTANCE
    while travelLengthLeft>TRAVEL_LENGTH_THRESHOLD:
        if travelLengthLeft<GPS_POINT_DISTANCE:
            travelStep=travelLengthLeft
        lastRoutePosition.coordinates.longitude = lastRoutePosition.coordinates.longitude + (travelStep * cos(lastRoutePosition.direction))
        lastRoutePosition.coordinates.latitude = lastRoutePosition.coordinates.latitude + (travelStep * sin(lastRoutePosition.direction))
        gpsPoints.append(copy.deepcopy(lastRoutePosition.coordinates))
        travelLengthLeft-=travelStep
    return lastRoutePosition, gpsPoints

def getCirclePosition(center, radius, angle):
    pos=GPS(0, 0)
    pos.longitude = center.longitude + radius * cos(angle)
    pos.latitude = center.latitude   + radius * sin(angle)
    return pos
#longitude is x
#latitude is y
def travelCurve(routePosition, roadSectionCurve, useAngle = False):
    turnAngle=Decimal(math.radians(roadSectionCurve.length))
    if roadSectionCurve.turn==TurnDirection.LEFT:
        direction=-1
    else:
        direction=1
    [x, y, c] = generateTurn(routePosition.coordinates.longitude, routePosition.coordinates.latitude, routePosition.direction, direction, roadSectionCurve.radius, turnAngle)
    lastRoutePosition=RoutePosition(GPS(x[-1], y[-1]), routePosition.direction-direction*turnAngle)
    gpsPoints=list()
    for i in range(len(x)):
        gpsPoints.append(GPS(x[i], y[i]))
    return lastRoutePosition, gpsPoints, c
# def travelCircle(routePosition, roadSectionCurve, useAngle = False):
#     lastRoutePosition=RoutePosition(routePosition.coordinates, routePosition.direction)
#     curve = GroundTruthCurve(-1, None, None, None)
#     centerDirection=lastRoutePosition.direction
#
#     if roadSectionCurve.turn==TurnDirection.LEFT:
#         angleDirection = 1
#     else:
#         angleDirection = -1
#     centerDirection = (centerDirection + (angleDirection * PI / 2))
#     center=GPS(0, 0)
#     center.longitude = routePosition.coordinates.longitude + (roadSectionCurve.radius * cos(centerDirection))
#     center.latitude = routePosition.coordinates.latitude + (roadSectionCurve.radius * sin(centerDirection))
#     curve.pc = routePosition.coordinates
#     curve.center = center
#     curve.type = CurveType.SIMPLE
#
#     lastCenterToOuterDirection = (lastRoutePosition.direction  - (angleDirection * PI/2))
#     #origPos = getCirclePosition(center, roadSectionCurve.radius, lastCenterToOuterDirection)
#     #assert origPos.longitude == routePosition.coordinates.longitude
#     gpsPoints=[]
#
#     if useAngle:
#         minDistance = Decimal(GPS_POINT_DISTANCE) / roadSectionCurve.radius
#         travelStepAngle = angleDirection * minDistance
#         travelLengthLeft = Decimal(math.radians(roadSectionCurve.length))
#         minTravelThreshold = TRAVEL_LENGTH_THRESHOLD / roadSectionCurve.radius
#     else:
#         minDistance = Decimal(GPS_POINT_DISTANCE)
#         travelStepAngle = angleDirection*minDistance / roadSectionCurve.radius
#         travelLengthLeft = roadSectionCurve.length
#         minTravelThreshold = TRAVEL_LENGTH_THRESHOLD
#     minTravelThreshold=0
#     while travelLengthLeft > minTravelThreshold:
#         if travelLengthLeft < minDistance:
#             if useAngle:
#                 travelStepAngle = angleDirection * travelLengthLeft
#             else:
#                 travelStepAngle = angleDirection * travelLengthLeft  / (roadSectionCurve.radius)
#         lastCenterToOuterDirection+=travelStepAngle
#         newPos = getCirclePosition(center, roadSectionCurve.radius, lastCenterToOuterDirection)
#         d = getDistance(lastRoutePosition.coordinates, newPos)
#         if useAngle:
#             travelLengthLeft -= abs(travelStepAngle)
#         else:
#             travelLengthLeft-=d
#         #assert travelLengthLeft>=0
#         lastRoutePosition.coordinates=newPos
#         lastRoutePosition.direction= lastCenterToOuterDirection  + (angleDirection * PI/2)
#         gpsPoints.append(newPos)
#     curve.pt=gpsPoints[-1]
#     return lastRoutePosition, gpsPoints, curve
#
# def travelTransition(routePosition, r, alpha, n, turn_direction, reverse):
#     return
# def travelCurve(routePosition, roadSectionCurve, useAngle=False):
#     return
#


def transition(x_init, y_init, dir_init, turn_direction, r, alpha, reverse=None, n=None):
    # draw eular spiral if spiral starts at radius at infinity and ends at
    # radius 'r' if reverse=false and vice versa
    diff = 0

    Rx = [[cos(dir_init + diff), -sin(dir_init + diff)]]
    Ry = [[sin(dir_init + diff), cos(dir_init + diff)]]

    L = 2 * r * alpha

    # step=L / (n - 1)
    step = Decimal(GPS_POINT_DISTANCE)
    rem = L % step
    if rem >= (step / 2):
        n = L // step
        n += 1
        step = L / n

    s = rangeI(0, L, step)

    fx = lambda v: (v - ((v ** 5) / (40 * (r ** 2) * (L ** 2))))
    fy = lambda v: ((v ** 3) / (6 * r * L) - ((v ** 7) / (336 * (r ** 3) * (L ** 3))))
    x = apply(s, fx)
    y = apply(s, fy)
    negFunc = lambda v: -v

    if turn_direction == 1:
        # turn the transition to the right
        y = apply(y, negFunc)

    if reverse:
        # draw eular spiral if spiral starts at radius 'r' and ends at infinity
        x = apply(x, negFunc)
        xdiff = x[-1] - x[0]
        f1 = lambda v: (v - xdiff)
        x = apply(x, f1)

        ydiff = y[-1] - y[0]
        f2 = lambda v: (v - ydiff)
        y = apply(y, f2)

        x.reverse()
        y.reverse()

    t = 4
    t = 0
    h = x[-1 - t] - (r * sin(alpha))
    k = y[-1 - t] + (r * cos(alpha))
    if turn_direction == 1:
        h = x[-1 - t] - (r * sin(alpha))
        k = y[-1 - t] - (r * cos(alpha))

    f1 = lambda v: (x_init + v)
    f2 = lambda v: (y_init + v)
    coord = [x, y]
    x = apply(matMul(Rx, coord), f1)[0]
    y = apply(matMul(Ry, coord), f2)[0]

    coord = [[h], [k]]
    h = apply(matMul(Rx, coord), f1)[0][0]
    k = apply(matMul(Ry, coord), f2)[0][0]
    return [x, y, h, k]


def generateTurn(x_init,y_init,dir_init,turn_direction,r,angle):
    gtcurve = GroundTruthCurve(-1, None, None, None)
    gtcurve.transitionPC = GPS(x_init, y_init)
    #TODO check if I'm setting the PC and PT correctly for the curve
    #right now we define the transition section as 1/8 of the angle
    pc_angle=angle / 8
    pt_angle=pc_angle
    curve_angle= angle - (pc_angle + pt_angle)
    [x,y,h,k]=transition(x_init,y_init,dir_init,turn_direction,r,pc_angle,False)

    gtcurve.pc = GPS(x[-1], y[-1])
    gtcurve.center = GPS(h, k)

    gtcurve.type = CurveType.SIMPLE

    if turn_direction == 1:
        [xp,yp]=circle(h,k,dir_init- pc_angle,turn_direction,r,PI / 2,PI / 2  - curve_angle)
    else:
        [xp,yp]=circle(h,k,dir_init+ pc_angle,turn_direction,r,- PI / 2,-PI / 2 + curve_angle)
    #gtcurve.pc = GPS(xp[0], yp[0])

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