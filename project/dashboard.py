import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
from collections import deque

filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::DashboardDomain",  filepath + "/DDS.xml")
microphone_input = connector.getInput("DashboardSubscriber::DashboardMicrophoneReader")
sensors_input = connector.getInput("DashboardSubscriber::DashboardTemperatureReader")
actuator_input = connector.getInput("DashboardSubscriber::DashboardActuatorReader")

temperature_sensor1 = []
temperature_sensor2 = []
extreme_temperature_deque_1 = deque(maxlen=10)
extreme_temperature_deque_2 = deque(maxlen=10)


def read_mic_content():
    microphone_input.read()
    num_of_samples = microphone_input.samples.getLength()
    for j in range(0, num_of_samples):
        if microphone_input.infos.isValid(j):
            some_string = microphone_input.samples.getString(j, "Content")
            print(f'Microphone: The time now is {some_string}')


def arrange_temperatures():
    temperature_sensor1.clear()
    temperature_sensor2.clear()
    sensors_input.read()
    all_temperatures = sensors_input.samples.getLength()
    for i in range(0, all_temperatures):
        if sensors_input.infos.isValid(i):
            temp1 = sensors_input.samples.getNumber(i, "Sensor1")
            temp2 = sensors_input.samples.getNumber(i, "Sensor2")
            if temp1 > 1:
                temperature_sensor1.append(temp1)
            elif temp2 > 1:
                temperature_sensor2.append(temp2)
    find_extreme()


def find_extreme():
    extreme_temperature_deque_1.clear()
    extreme_temperature_deque_2.clear()
    for k in reversed(range(0, min(len(temperature_sensor1), len(temperature_sensor2)))):
        temp1 = temperature_sensor1[len(temperature_sensor1) - k - 1]
        temp2 = temperature_sensor2[len(temperature_sensor2) - k - 1]
        dif = abs(temp1 - temp2)
        if dif > 8:
            extreme_temperature_deque_1.append(temp1)
            extreme_temperature_deque_2.append(temp2)
    if len(extreme_temperature_deque_1) == 0:
        print("No extreme temperature difference have been measured.")
    else:
        print("Thermometer 1: Extreme temperature")
        print("{:<10}{}".format("Sample #", "Status"))
        print("-" * 22)
        for i, value in enumerate(extreme_temperature_deque_1):
            print("{:<10}{}".format(i+1, value))
        print("Thermometer 2: Extreme temperature")
        print("{:<10}{}".format("Sample #", "Status"))
        print("-" * 22)
        for i, value in enumerate(extreme_temperature_deque_2):
            print("{:<10}{}".format(i+1, value))


def read_actuator_status():
    actuator_input.read()
    num_of_samples = actuator_input.samples.getLength()
    print("Actuator: Last 10 Actuator status")
    print("{:<10}{}".format("Sample #", "Status"))
    print("-"*22)
    for j in range(0, num_of_samples):
        if actuator_input.infos.isValid(j):
            some_string = actuator_input.samples.getString(j, "Status")
            print("{:<10}{}".format(j+1, some_string))
    print()


def calibration_time():
    actuator_input.read()
    time = "No calibration happened"
    all_times = actuator_input.samples.getLength()
    for i in range(0, all_times):
        if actuator_input.infos.isValid(i):
            time = actuator_input.samples.getString(i, "Time")
    print(f"The last calibration's time: {time}\n")


while True:
    calibration_time()
    sleep(1)
    read_mic_content()
    read_actuator_status()
    arrange_temperatures()
    sleep(5)
