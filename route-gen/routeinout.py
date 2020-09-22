from fileio import *
from routemodel import *
from curvemodel import *
from decimal import Decimal
import routeconstants

def importRouteGenPlan(routePlanFile):
    plan=[]
    data = readCSVFile(routePlanFile)
    for row in data:
        sectionType=RoadSectionType[row[routeconstants.INDEX_PLAN_TYPE].upper()]
        #print("reading..."+str(sectionType))
        if sectionType == RoadSectionType.START:
            plan.append(RoutePosition(GPS(Decimal(row[routeconstants.INDEX_PLAN_START_LONGITUDE]),
                                              Decimal(row[routeconstants.INDEX_PLAN_START_LATITUDE])),
                                          Decimal(row[routeconstants.INDEX_PLAN_START_DIRECTION])))
        elif sectionType==RoadSectionType.LINE:
            plan.append(RoadSectionLine(Decimal(row[routeconstants.INDEX_PLAN_LENGTH])))
        elif sectionType==RoadSectionType.CURVE:
            plan.append(RoadSectionCurve(TurnDirection[row[routeconstants.INDEX_PLAN_TRAVEL_DIR].upper()], Decimal(row[routeconstants.INDEX_PLAN_RADIUS]), Decimal(row[routeconstants.INDEX_PLAN_LENGTH])))
    return plan

def exportGPSPointsToList(gpsPoints):
    csvLines=list()
    i=0
    for p in gpsPoints:
        r=list()
        r.append(i)
        r.append(p.longitude)
        r.append(p.latitude)
        csvLines.append(r)
        i+=1
    return csvLines

def exportGTCurvesToList(curves):
    csvLines=list()
    i=0
    for curve in curves:
        r=list()
        r.append(i)
        r.append(curve.center.longitude)
        r.append(curve.center.latitude)
        r.append(curve.pc.longitude)
        r.append(curve.pc.latitude)
        r.append(curve.pt.longitude)
        r.append(curve.pt.latitude)
        r.append(curve.type.name)
        r.append(curve.group)
        csvLines.append(r)
        i+=1
    return csvLines

def exportGTCurvesToFile(gtCurves, gtCurveFile):
    csvLines=exportGTCurvesToList(gtCurves)
    csvLines.insert(0, ['ID','Center X', 'Center Y', 'PC X', 'PC Y', 'PT X', 'PT Y', 'CLASSIFICATION', 'GROUP ID'])
    writeCSVFile(csvLines, gtCurveFile)

def exportGPSPointsToFile(gpsPoints, gpsPointFile):
    csvLines=exportGPSPointsToList(gpsPoints)
    csvLines.insert(0, ['ID','longitude', 'latitude'])
    writeCSVFile(csvLines, gpsPointFile)
