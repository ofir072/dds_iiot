# DDS IOT Project

`actuator.py` - The actuator script. Read the temperature display by the sensors and button state, and write his current status.

`button.py` - The button script. Only write his current state.

`dashboard.py` - The dashboard script. Read the actuator status, the temperatures display by the sensors and the microphone message.

`microphone.py` - The microphone script. Only write his current message.

`sensor1.py` - The sensor1 script - temperature thermometer. Write to the temperature topic and read the actuator status.

`sensor2.py` - The sensor2 script - temperature thermometer. Write to the temperature topic and read the actuator status.

`sensor3.py` - The sensor3 script - temperature thermometer. Only write his temperature input.

`DDS.xml` - The definition of the different domains we use in the scripts mentioned above, the QoS rules for application needs, and the topic & types the system have.

For the sake of clarity and ease of understanding, I have created some markdowns:

    1.  After a single extreme temperature difference, the actuator will move to a degraded state, and after two measured differences, it will stop completely.
        To understand the assignment guidelines, I followed the flow chart provided
    2.  The dashboard displays the last 10 extreme differences without any context of when the last calibration was performed.
        This is in accordance with the guideline that states:
            'The Dashboard shall display the last 10 measurements only of an extreme temperature difference from Temperature sensor 1 and from Temperature sensor 2
             (even if the dashboard was initialized after the sensors sent their last status messages).'
        The note (1) also specifies that the dashboard should display the last 10 without regard to the extreme differences. Therefore, I decided to implement the first line of instructions given.