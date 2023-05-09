import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep, time
import random

filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Sensor2Domain", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Sensor2Publisher::Sensor2Writer")

while True:
    randomTemp = random.randint(-6, 6) + 23
    status = '[ok]'
    outputDDS.instance.setNumber("Sensor2", randomTemp)
    outputDDS.write()
    print(f'published: {randomTemp}, status: {status}')
    sleep(0.1)


