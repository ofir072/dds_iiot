import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
from collections import deque

filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::DashboardDomain",  filepath + "/DDS.xml")
microphone_input = connector.getInput("DashboardSubscriber::DashboardMicrophoneReader")
sensors_input = connector.getInput("DashboardSubscriber::DashboardTemperatureReader")

extreme_temperature_deque1 = deque(maxlen=10)
extreme_temperature_deque2 = deque(maxlen=10)

while True:

    # microphone_input.read()
    # numOfSamples = microphone_input.samples.getLength()
    # print(f'numOfSamples: {numOfSamples}')
    # for j in range(0, numOfSamples):
    #     if microphone_input.infos.isValid(j):
    #         some_string = microphone_input.samples.getString(j, "Content")
    #         print(f'Received Example: Time: {some_string}')

    sensors_input.read()
    numOfSamples = sensors_input.samples.getLength()
    print(f'numOfSamples: {numOfSamples}')
    for j in range(0, numOfSamples):
        if sensors_input.infos.isValid(j):
            temperature1 = sensors_input.samples.getNumber(j, "Sensor1")
            temperature2 = sensors_input.samples.getNumber(j, "Sensor2")
            print(temperature1, temperature2)

    #       gap = abs(temperature2-temperature1)
    #         if gap >= 8:
    #             extreme_temperature_deque1.append(temperature1)
    #             extreme_temperature_deque1.append(temperature2)
    # print("Sensor1", " " * 3, "Sensor2", " " * 3, "Gap")
    # for x, y in zip(extreme_temperature_deque1, extreme_temperature_deque2):
    #     print("{:<10}{}{:>10}".format(x, " " * 3, y), " " * 3, abs(x-y))

    sleep(1)
