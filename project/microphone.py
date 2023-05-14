import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

from datetime import datetime

filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::MicrophoneDomain", filepath + "/DDS.xml")
outputDDS = connector.getOutput("MicrophonePublisher::MicrophoneWriter")

while True:
    now = datetime.now()
    status = '[ok]'
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")           # Arrange the current date in ****/**/** **:**:** form
    outputDDS.instance.setString("Content", formatted_now)
    outputDDS.write()                                           # The writing to the "Message" topic
    print(f'Published time: {formatted_now}, Status: {status}')
    sleep(0.1)
