# ROS
The boat will use [ROS](https://ros.org/) to aid in the autonomous features and serve as a platform for future improvements.

On the boat, ROS Jazzy will be running on the RPi 4 on Ubuntu 24.04. For a basic introduction to ROS2 and tutorials for Jazzy, see [here](https://docs.ros.org/en/jazzy/).

## Initial Setup
Install Ubuntu 24.04 Server on the Raspberry Pi using the Raspberry Pi Imager.

Edit `/etc/apt/sources.list.d/ubuntu.sources` 
Change 
```Suites: noble```
To:
```Suites: noble noble-updates```

Install ROS2 Jazzy with **[these](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)** instructions.

Edit `~/.bashrc` by adding `source /opt/ros/jazzy/setup.bash` to the end.



## Install Packages:
```bash
sudo apt install ros-jazzy-mavros ros-jazzy-mavros-msgs ros-jazzy-sensor-msgs
```


## Install package
Assuming the parent repo is cloned at ~/RCCF_PEP:
```bash
mkdir ~/ros_ws
ln -s ~/RCCF_PEP/ROS ~/ros_ws/src
cd ros_ws
colcon build --symlink-install
echo "source ~/ros_ws/install/setup.bash" >> ~/.bashrc
bash
```




# About this setup
## Included Packages:
### adnav-ros2:
Set up from Advanced Navigation to use the Spatial IMU/GNSS

### vesc:
Package to communicate with the vesc to read main battery usage and motor data.

### tidebreaker:
Custom package to manage launching all relevant nodes.
Custom scripts;
- send_gps_to_ardupilot: Send the GPS/velocity data from adnav_node to the flight controller using the mavros package.
