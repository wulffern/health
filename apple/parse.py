import pandas as pd
import xmltodict
import sys

import json
import sys
import os
from xml.etree.ElementTree import iterparse

l_ignore = {
    "HKQuantityTypeIdentifierBodyMassIndex",
    "HKQuantityTypeIdentifierHeight",
    #"HKQuantityTypeIdentifierBodyMass",
    #"HKQuantityTypeIdentifierHeartRate",
    "HKQuantityTypeIdentifierBodyFatPercentage",
    "HKQuantityTypeIdentifierStepCount",
    #"HKQuantityTypeIdentifierDistanceWalkingRunning",
    "HKQuantityTypeIdentifierBasalEnergyBurned",
    "HKQuantityTypeIdentifierActiveEnergyBurned",
    "HKQuantityTypeIdentifierFlightsClimbed",
    #"HKQuantityTypeIdentifierAppleExerciseTime",
    "HKQuantityTypeIdentifierDistanceCycling",
    "HKQuantityTypeIdentifierDistanceSwimming",
    "HKQuantityTypeIdentifierSwimmingStrokeCount",
    "HKQuantityTypeIdentifierWaistCircumference",
    "HKQuantityTypeIdentifierRestingHeartRate",
    "HKQuantityTypeIdentifierVO2Max",
    "HKQuantityTypeIdentifierWalkingHeartRateAverage",
    "HKQuantityTypeIdentifierHeadphoneAudioExposure",
    "HKQuantityTypeIdentifierAppleStandTime",
    "HKCategoryTypeIdentifierSleepAnalysis",
    "HKCategoryTypeIdentifierAppleStandHour",
    "HKCategoryTypeIdentifierMindfulSession",
    "HKCategoryTypeIdentifierHighHeartRateEvent",
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"
}


files = dict()


def openFile(key):
    f =  open(f"tmp/{key}.json","w")
    f.write("[\n")
    files[key] = f

def addToFile(key,elem,comma=True):
    f = files[key]
    if(comma):
        f.write(",")
    f.write(json.dumps(elem.attrib,indent=4))
    

def closeFile(key):
    f = files[key]
    f.write("\n]\n")
    f.close()

def listTypes(file):
    uniq = dict()
    for _, elem in iterparse(file):
        if elem.tag == "Record":
            t_health = elem.attrib["type"]
            if(t_health not in uniq):
                uniq[t_health] = 1
                print(t_health)
            else:
                uniq[t_health] += 1
    print(json.dumps(uniq,indent=4))
    
def main(file):
    for _, elem in iterparse(file):
        if elem.tag == "Record":
            t_health = elem.attrib["type"]
            if(t_health not in l_ignore):
                if(t_health not in files):
                    openFile(t_health)
                    addToFile(t_health,elem,comma=False)
                else:
                    addToFile(t_health,elem)
    for key in files:
        closeFile(key)

if(len(sys.argv) > 0):
     main(sys.argv[1])
else:
    print("Error: parse.py <export.xml from apple health export>")
