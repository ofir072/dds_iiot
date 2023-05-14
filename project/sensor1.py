import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep, time
import random

filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Sensor1Domain", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Sensor1Publisher::Sensor1Writer")
inputDDS = connector.getInput("Sensor1Subscriber::Sensor1Reader")


# Read the actuator current status
def actuator_status():
    inputDDS.read()
    some_string = ""
    num_of_samples = inputDDS.samples.getLength()
    for j in range(0, num_of_samples):
        if inputDDS.infos.isValid(j):
            some_string = inputDDS.samples.getString(j, "Status")
    return some_string


while True:
    randomTemp = random.randint(-6, 6) + 23     # The temperature sensor1 will display
    status = '[ok]'
    outputDDS.instance.setNumber("Sensor1", randomTemp)
    outputDDS.write()
    if not actuator_status() == "Stopped":      # Print temperature to console only if the actuator is not "Stopped"
        print(f'published: {randomTemp}, status: {status}')     # The self console prints
    sleep(0.1)
