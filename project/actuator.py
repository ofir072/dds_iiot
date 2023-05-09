import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::ActuatorDomain",  filepath + "/DDS.xml")
button_input = connector.getInput("ActuatorSubscriber::ActuatorButtonReader")
sensors_input = connector.getInput("ActuatorSubscriber::ActuatorTemperatureReader")


def button_command():    # Get the button command
    button_input.read()
    num_of_samples = button_input.samples.getLength()
    print(f'numOfSamples: {num_of_samples}')
    for j in range(0, num_of_samples):
        if button_input.infos.isValid(j):
            some_string = button_input.samples.getString(j, "Condition")
            print(f'Received Example: Button condition: {some_string}')
            if some_string == "Stop":
                return True
    return False


def temperature_measurement():
    last_temp1 = 0
    last_temp2 = 0
    sensors_input.read()
    all_temperatures = sensors_input.samples.getLength()
    for i in range(0, all_temperatures):
        if sensors_input.infos.isValid(i):
            temp1 = sensors_input.samples.getNumber(i, "Sensor1")
            temp2 = sensors_input.samples.getNumber(i, "Sensor2")
            if temp1 > 1:
                last_temp1 = temp1
            elif temp2 > 1:
                last_temp2 = temp2
    dif = abs(last_temp2-last_temp1)
    if dif > 8:
        return True
    return False


def sensor3_measurement():
    sensors_input.read()
    all_temperatures = sensors_input.samples.getLength()
    for i in range(0, all_temperatures):
        if sensors_input.infos.isValid(i):
            temp3 = sensors_input.samples.getNumber(i, "Sensor3")
    return temp3


while True:
    status = "Working"
    if button_command():
        status = "Stopped"
        print("Received a stop command...")
        sleep(0.5)
        while button_command():
            sleep(0.1)
    if temperature_measurement() > 8:
        gap = temperature_measurement
        if gap > 8:
            status = "Degraded"
            print(f"Difference measured: {gap}, calibration thermometer measurement: {sensor3_measurement}")
            print("Calibration is needed...")
            sleep(0.5)

