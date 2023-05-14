import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep


filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::ButtonDomain", filepath + "/DDS.xml")
outputDDS = connector.getOutput("ButtonPublisher::ButtonWriter")


# Writing to the "Switch" topic the condition of the button
def output_and_write(condition, status):
    outputDDS.instance.setString("Condition", condition)
    outputDDS.write()
    print(f'Published switch condition: {condition}, Status: {status}')


while True:
    condition = "Start"
    status = '[ok]'
    output_and_write(condition, status)
    sleep(20)
    condition = "Stop"
    output_and_write(condition, status)
    sleep(5)
