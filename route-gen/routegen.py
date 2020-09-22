from routeinout import *
from routeutils import *
from curveutils import *
from gpsutils import *
from  constants import *
import argparse
import sys
import csv
import os



def classifyCurveGroup(count, gtCurves, groupId):
    curves = gtCurves[-count:]
    if curveCount == 2:
        if isCurvesSameDirection(curves[0], curves[1]):
            curveType = CurveType.COMPOUND
        else:
            curveType = CurveType.REVERSE
    else:
        curveType = CurveType.CONTINUOUS
    for curve in curves:
        curve.type = curveType
        curve.group = groupId


parser = argparse.ArgumentParser(description='Generate routes', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(metavar='route-file', dest='routeFile', nargs='?', help='Route plan csv file. \n'
                                                                            '"LINE, <Length>"\n '
                                                                            '\tor \n'
                                                                            '"CURVE, <Length>, <Turn_Direction>, <Radius>"')
parser.add_argument('-g', dest='gtFile', metavar='GroundTruth', nargs=1, help='Path to save the ground truth curve csv file')
parser.add_argument('-r', dest='gpsFile', metavar='GPSRoute', nargs=1, help='Path to save the GPS coordinates')
parser.add_argument('--start', dest='startVector', metavar='startVector', nargs=1, help='Starting position of the route. Format should be:\n'
                                                                                        '"(<longitude>,<latitude>,<angle_direction>)"')
parser.add_argument('--useAngle', dest='angle', default=False, action='store_true', help='Use the length as the angle (in degrees) for generating \nthe curve')
parser.add_argument('--plot', dest='plot', default=False, action='store_true', help='Visualize the gps route and the curves')



args = parser.parse_args()
if not args.routeFile:
    parser.print_usage()
    exit()

if len(sys.argv)<=1:
    print("file parameter missing")
    exit()

routeFile = sys.argv[1]
print("Importing route plan  from " + routeFile + "...", end='')
plannedRoute = importRouteGenPlan(routeFile)
print("done")
gpsPoints=list()
groundTruthCurves=list()


cwd = os.getcwd()
os.chdir(r"{}\samples".format(cwd))
with open('eggs.csv') as cv:
    reader = csv.reader(cv)
    row1 = next(reader)
    for rows in reader:
        a = rows[1]
        l = rows[3]
        break
os.chdir(cwd)


startLongitude = -(int(l) * cos(int(a)))
startLatitude = -(int(l) * sin(int(a)))
startAngleDirection=0

if args.startVector:
    import re
    numStr="[-+]?\d*\.\d*|[-+]?\d+"
    matchObj = re.search("^\(("+numStr+"),("+numStr+"),("+numStr+")\)$", args.startVector[0])
    if matchObj:
        startLongitude=Decimal(matchObj.group(1))
        startLatitude=Decimal(matchObj.group(2))
        startAngleDirection=Decimal(math.radians(Decimal(matchObj.group(3))))
    else:
        print("Incorrect format for start vector. Correct format is (<longitude>,<latitude>,<angle_direction>)")
        exit(0)

lastPosition = RoutePosition(GPS(startLongitude,startLatitude), startAngleDirection)
gpsPoints.append(lastPosition.coordinates)
curveCount=0
lastCurve=None
curveGroupId=0
distanceFromLastCurve=0
print("Creating route", end='')
for nextRoute in plannedRoute:
    print(".", end='')
    if nextRoute.type==RoadSectionType.LINE:
        lastPosition, traveledGPS = travelLine(lastPosition, nextRoute)
        if curveCount>0:
            distanceFromLastCurve+=nextRoute.length
    elif nextRoute.type==RoadSectionType.CURVE:
        lastPosition, traveledGPS, curve = travelCurve(lastPosition, nextRoute, args.angle)
        groundTruthCurves.append(curve)
        curveCount+=1
        distanceFromLastCurve=0

    if distanceFromLastCurve>THRESHOLD_ADJACENT_CURVE_DISTANCE:
        if curveCount > 1:
            classifyCurveGroup(curveCount, groundTruthCurves, curveGroupId)
            curveGroupId+=1
        curveCount=0
        distanceFromLastCurve=0
    gpsPoints = gpsPoints + traveledGPS
if curveCount > 1:
    classifyCurveGroup(curveCount, groundTruthCurves, curveGroupId)
    curveGroupId += 1
print("done")

if args.gpsFile:
    print("Exporting GPS points ("+str(len(gpsPoints))+" coordinates) to "+args.gpsFile[0]+"...", end='')
    exportGPSPointsToFile(gpsPoints, args.gpsFile[0])
    print("done")
else:
    print("GPS points")
    printTable(exportGPSPointsToList(gpsPoints))
    print()

if args.gtFile:
    print("Exporting curve list (" + str(len(groundTruthCurves)) + " curves) to " + args.gtFile[0] + "...", end=''),
    exportGTCurvesToFile(groundTruthCurves, args.gtFile[0])
    print("done"),
else:
    print("Ground Truth Curves")
    printTable(exportGTCurvesToList(groundTruthCurves))
    print()

if args.plot:
    import matplotlib.pyplot as plt

    mpl_fig = plt.figure()
    plotGPSPoints(gpsPoints, plt)
    plotGTCurves(groundTruthCurves, plt)

    plt.axis('scaled')
    plt.show()