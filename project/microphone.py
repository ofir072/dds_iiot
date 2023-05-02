import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

from datetime import datetime

filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::MicrophoneDomain", filepath + "/DDS.xml")
outputDDS = connector.getOutput("MicrophonePublisher::MicrophoneWriter")

while True:
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    outputDDS.instance.setString("Message", formatted_now)
    outputDDS.write()
    sleep(1)

