import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
from collections import deque

# Get the current file path and create a Connector object with the specified XML configuration
filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::DashboardDomain", filepath + "/DDS.xml")

# Get Input objects for the three topics
microphone_input = connector.getInput("DashboardSubscriber::DashboardMicrophoneReader")
sensors_input = connector.getInput("DashboardSubscriber::DashboardTemperatureReader")
actuator_input = connector.getInput("DashboardSubscriber::DashboardActuatorReader")

# Initialize lists and deques for storing temperature readings
temperature_sensor1 = []
temperature_sensor2 = []
extreme_temperature_deque_1 = deque(maxlen=10)
extreme_temperature_deque_2 = deque(maxlen=10)


# Reads and prints the content of the "Message" topic
def read_mic_content():
    microphone_input.read()
    num_of_samples = microphone_input.samples.getLength()
    for j in range(0, num_of_samples):
        if microphone_input.infos.isValid(j):
            some_string = microphone_input.samples.getString(j, "Content")
            print(f'Microphone: The time now is {some_string}')


# Reads and arranges the temperature readings from two temperature sensors (Sensor1 and Sensor2)
def arrange_temperatures():
    temperature_sensor1.clear()
    temperature_sensor2.clear()
    sensors_input.read()
    all_temperatures = sensors_input.samples.getLength()
    for i in range(0, all_temperatures):
        if sensors_input.infos.isValid(i):
            temp1 = sensors_input.samples.getNumber(i, "Sensor1")
            temp2 = sensors_input.samples.getNumber(i, "Sensor2")
            # Only consider temperatures that are greater than 1 (throw empty writing)
            if temp1 > 1:
                temperature_sensor1.append(temp1)
            elif temp2 > 1:
                temperature_sensor2.append(temp2)
    find_extreme()


# Finds the extreme temperature difference between the two temperature sensors
def find_extreme():
    extreme_temperature_deque_1.clear()
    extreme_temperature_deque_2.clear()
    for k in reversed(range(0, min(len(temperature_sensor1), len(temperature_sensor2)))):
        temp1 = temperature_sensor1[len(temperature_sensor1) - k - 1]
        temp2 = temperature_sensor2[len(temperature_sensor2) - k - 1]
        dif = abs(temp1 - temp2)
        # Store temperatures with a difference greater than 8 in the deques
        if dif > 8:
            extreme_temperature_deque_1.append(temp1)
            extreme_temperature_deque_2.append(temp2)
    if len(extreme_temperature_deque_1) == 0:
        print("No extreme temperature difference has been measured.")
    # Print the values of the two sensors
    else:
        print("Thermometer 1: Extreme temperature")
        print("{:<10}{}".format("Sample #", "Temperature"))
        print("-" * 22)
        for i, value in enumerate(extreme_temperature_deque_1):
            print("{:<10}{}".format(i+1, value))
        print("Thermometer 2: Extreme temperature")
        print("{:<10}{}".format("Sample #", "Temperature"))
        print("-" * 22)
        for i, value in enumerate(extreme_temperature_deque_2):
            print("{:<10}{}".format(i+1, value))


# Reads and prints the content of the "ActuatorStatus" topic to get the last 10 status changes
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


# Reads and prints the content of the "ActuatorStatus" topic to get the last calibration time
def calibration_time():
    actuator_input.read()
    time = "No calibration happened."
    all_times = actuator_input.samples.getLength()
    for i in range(0, all_times):
        if actuator_input.infos.isValid(i):
            if not actuator_input.samples.getString(i, "Time") == "":
                time = actuator_input.samples.getString(i, "Time")
    print(f"The last calibration's time: {time}\n")


while True:
    read_mic_content()
    read_actuator_status()
    arrange_temperatures()
    calibration_time()
    sleep(5)
