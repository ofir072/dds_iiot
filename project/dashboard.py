import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
from collections import deque

filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::DashboardDomain",  filepath + "/DDS.xml")
microphone_input = connector.getInput("DashboardSubscriber::DashboardMicrophoneReader")
sensors_input = connector.getInput("DashboardSubscriber::DashboardTemperatureReader")

temperature_sensor1 = []
temperature_sensor2 = []
extreme_temperature_deque = deque(maxlen=10)


def read_mic_content():
    microphone_input.read()
    num_of_samples = microphone_input.samples.getLength()
    print(f'numOfSamples: {num_of_samples}')
    for j in range(0, num_of_samples):
        if microphone_input.infos.isValid(j):
            some_string = microphone_input.samples.getString(j, "Content")
            print(f'Received Example: Time: {some_string}')


def arrange_temperatures():
    sensors_input.read()
    all_temperatures = sensors_input.samples.getLength()
    print(f'numOfSamples: {all_temperatures}')
    for i in range(0, all_temperatures):
        if sensors_input.infos.isValid(i):
            temperature_sensor1.append(sensors_input.samples.getNumber(i, "Sensor1"))
            temperature_sensor2.append(sensors_input.samples.getNumber(i, "Sensor2"))
    find_extreme()


def find_extreme():
    extreme_temperature_deque.clear()
    for k in reversed(range(0, min(len(temperature_sensor1), len(temperature_sensor2)))):
        dif = abs(temperature_sensor1[len(temperature_sensor1) - k - 1] - temperature_sensor2[len(temperature_sensor2) - k - 1])
        if dif > 8:
            extreme_temperature_deque.appendleft(dif)
    if len(extreme_temperature_deque) == 0:
        print("No extreme temperature difference have been measured.")
    else:
        print("The last 10 extreme temperature difference that have been measured:")
        for i, value in enumerate(extreme_temperature_deque):
            print(f"Index {i + 1}:  {value}")


while True:
    # read_mic_content()
    arrange_temperatures()
    sleep(1)

