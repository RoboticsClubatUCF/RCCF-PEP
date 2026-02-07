## RCCF-PEP25
All code for RCCF's PEP 25 Competition Boat

# About:
The boat is be controlled by [ArduRover](https://ardupilot.org/rover/). The onboard flight controller is a [CubePilot Orange](https://ardupilot.org/copter/docs/common-thecubeorange-overview.html).

Learn how to install Mission Planner [here](https://ardupilot.org/planner/docs/mission-planner-installation.html). When the CubePilot is connected to a computer in Mission Planner, the latest version of ArduRover can be installed. Download the [parameters](PEP25ArdupilotParameters.param) and upload them to the Board in Mission Planner.

ESP32-PWM-to-Stepper is a hack to allow for the rudder to be controlled with a stepper motor rather than a servo.


## Installation:
This will install all of the code in a GIT workspace on your computer.

Find instructions on adding an ssh key [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

```bash
mkdir "RCCF PEP 2025"
cd "RCCF PEP 2025"
mkdir src
git clone git@github.com:RoboticsClubatUCF/RCCF-PEP25.git src
cd src
git submodule update --init --recursive
```

## In This Repository:
- ArduPilot Stuff:
	- Ardupilot parameter list
	- Lua scripts to allow for arm/disarming of the relay and for a reverse switch on the controller
- [ESP32 PWM to Stepper](https://github.com/RoboticsClubatUCF/ESP32-PWM-to-Stepper/tree/8160392d6b5879aeb35a627ed0b1841411643998)
	- Rudder control
- ROS and RPi Stuff
- Electrical
	- Images/guides to electrical systems
	- [VESC Guide](Electrical/VESCguide.md)






## Goals:
- Reliable RC Control of Boat
- CAN BUS communication with ESC
- Autonomous waypoint following
	- Looking at connecting a USB GPS to RPi and forwarding that data via MavLink
- WiFi based communications:
	- Camera stream
	- Temperature sensors on high power components
	- Battery voltage and current monitoring
- Later: Telemetry Radio


## Issues:
- The stepper motor is a weird hack that introduces an extra point of failure. Ideally, an actual servo would be used. 
- This year we struggled with not testing software/electrical sytems sooner. Emphasize testing subsystems as you go but understand there will still be unexpected issues when doing a full systems integration.
