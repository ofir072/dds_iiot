from datetime import datetime
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

filepath = osPath.dirname(osPath.realpath(__file__))

# Get input and output from the connector
connector = rti.Connector("MyParticipantLibrary::ActuatorDomain",  filepath + "/DDS.xml")
button_input = connector.getInput("ActuatorSubscriber::ActuatorButtonReader")
sensors_input = connector.getInput("ActuatorSubscriber::ActuatorTemperatureReader")
actuator_output = connector.getOutput("ActuatorPublisher::ActuatorWriter")

actuator_status = "Working"
heat_stop = False


# Get the button command condition from the "Switch" topic
def button_command():
    global heat_stop
    button_input.read()
    num_of_samples = button_input.samples.getLength()
    for j in range(0, num_of_samples):
        if button_input.infos.isValid(j):
            some_string = button_input.samples.getString(j, "Condition")
            # Return False if the switch is off
            if some_string == "Stop":
                heat_stop = False
                return True
    return False


# Reads and arranges the temperature readings from two temperature sensors (Sensor1 and Sensor2)
def temperature_measurement(k):
    last_temp1 = 0
    last_temp2 = 0
    sensors_input.read()
    all_temperatures = sensors_input.samples.getLength()
    for i in range(0, all_temperatures-k):
        if sensors_input.infos.isValid(i):
            temp1 = sensors_input.samples.getNumber(i, "Sensor1")
            temp2 = sensors_input.samples.getNumber(i, "Sensor2")
            # Only consider temperatures that are greater than 1 (throw empty writing)
            if temp1 > 1:
                last_temp1 = temp1
            elif temp2 > 1:
                last_temp2 = temp2
    #  Return the absolute gap between them
    return abs(last_temp2-last_temp1)


# Get the temperature measurement of sensors 3 from the "Temperature" topic
def sensor3_measurement():
    sensors_input.read()
    temp3 = 0
    all_temperatures = sensors_input.samples.getLength()
    for i in range(0, all_temperatures):
        if sensors_input.infos.isValid(i):
            if sensors_input.samples.getNumber(i, "Sensor3") > 0:
                temp3 = sensors_input.samples.getNumber(i, "Sensor3")
    return temp3


# Main loop
while True:

    # Check for button command
    if button_command() or heat_stop:
        actuator_status = "Stopped"
        actuator_output.instance.setString("Status", actuator_status)
        actuator_output.write()
        if not heat_stop:
            print(f"Status: {actuator_status}, Note: Received a stop command...\n")
        else:
            print(f"Status: {actuator_status}, Note: Waiting for restart...")

    # Check temperature measurement and calibrate if necessary
    elif temperature_measurement(0) > 8:    # 1st extreme difference
        gap = temperature_measurement(2)
        # No more extreme difference in 2nd check
        if gap < 8:
            # Set the actuator status
            actuator_status = "Degraded"
            actuator_output.instance.setString("Status", actuator_status)
            # Set the calibration time
            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            actuator_output.instance.setString("Time", formatted_time)
            actuator_output.write()
            print(f"Status: {actuator_status}, Note: Calibration is needed...")
            sleep(0.5)
            # Back to work after calibration
            actuator_status = "Working"
            actuator_output.instance.setString("Status", actuator_status)
            actuator_output.write()
            print(f"Status: {actuator_status}, Note: W-O-R-K-I-N-G-!\n")
        # 2nd extreme difference wait for restart
        else:
            print(f"Difference measured: {gap}, calibration thermometer measurement: {sensor3_measurement()}")
            heat_stop = True
    # All condition correct - keep\back working!
    else:
        actuator_status = "Working"
        actuator_output.instance.setString("Status", actuator_status)
        actuator_output.write()
        print(f"Status: {actuator_status}, Note: W-O-R-K-I-N-G-!\n")
    sleep(1)
