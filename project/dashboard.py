import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::DashboardDomain",  filepath + "/DDS.xml")
input_DDS = connector.getInput("DashboardSubscriber::DashboardWriter")

while True:
    input_DDS.take()
    numOfSamples = input_DDS.samples.getLength()
    print(f'numOfSamples: {numOfSamples}')
    for j in range(0, numOfSamples):
        if input_DDS.infos.isValid(j):
            some_string = input_DDS.samples.getString(j, "Message")
            print(f'Received Example: Status: {some_string}')
    sleep(1)



