import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep, time
import random

filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Sensor3Domain", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Sensor3Publisher::Sensor3Writer")

while True:
    randomTemp = random.randint(-1, 1) + 23
    status = '[ok]'
    outputDDS.instance.setNumber("Sensor3", randomTemp)
    outputDDS.write()
    print(f'published: {randomTemp}, status: {status}')
    sleep(1)


