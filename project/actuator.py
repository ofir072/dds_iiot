import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::ActuatorDomain",  filepath + "/DDS.xml")
input_DDS = connector.getInput("ActuatorSubscriber::ActuatorReader")

while True:
    input_DDS.take()
    numOfSamples = input_DDS.samples.getLength()
    print(f'numOfSamples: {numOfSamples}')
    for j in range(0, numOfSamples):
        if input_DDS.infos.isValid(j):
            some_string = input_DDS.samples.getString(j, "Message")
            print(f'Received Example: Time: {some_string}')
    sleep(1)


