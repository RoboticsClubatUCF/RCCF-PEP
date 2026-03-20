#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Twist
from mavros_msgs.msg import GPSRAW
import time

class GPSToArdupilot(Node):
    """
    ROS2 node that subscribes to a USB GPS NavSatFix topic and forwards
    the GPS data to ArduPilot via MAVRos GPS_INPUT mavlink message.
    """

    def __init__(self):
        super().__init__('gps_to_ardupilot_node')
        
        # Store latest twist data for velocity
        self.latest_twist = None
        
        # Subscribe to the GPS topic from the USB GPS
        self.gps_subscription = self.create_subscription(
            NavSatFix,
            '/adnav_node/nav_sat_fix',
            self.gps_callback,
            qos_profile=rclpy.qos.QoSProfile(depth=10)
        )
        
        # Subscribe to the velocity/twist topic from the Advanced Navigation IMU
        self.twist_subscription = self.create_subscription(
            Twist,
            '/adnav_node/twist',
            self.twist_callback,
            qos_profile=rclpy.qos.QoSProfile(depth=10)
        )
        
        # Publisher for GPS input to ArduPilot via MAVRos
        self.gps_input_pub = self.create_publisher(
            GPSRAW,
            '/mavros/gps_input/send',
            qos_profile=rclpy.qos.QoSProfile(depth=10)
        )
        
        self.get_logger().info('GPS to ArduPilot node initialized')
        self.get_logger().info(f'Subscribing to: /adnav_node/nav_sat_fix')
        self.get_logger().info(f'Subscribing to: /adnav_node/twist')
        self.get_logger().info(f'Publishing GPS_INPUT to: /mavros/gps_input/send')

    def gps_callback(self, msg: NavSatFix):
        """
        Callback function for incoming GPS data from NavSatFix topic.
        Converts NavSatFix message to GPSRAW message for ArduPilot.
        The latest velocity from the Twist topic is included if available.
        """
        # Create GPSRAW message for MAVRos
        gps_input = GPSRAW()
        
        # Set from NavSatFix message
        gps_input.latitude_deg = msg.latitude
        gps_input.longitude_deg = msg.longitude
        gps_input.altitude = msg.altitude
        gps_input.eph = 65535  # Horizontal dilution of precision (max value for unknown)
        gps_input.epv = 65535  # Vertical dilution of precision (max value for unknown)
        
        # Velocity components from Advanced Navigation IMU (filtered)
        # The IMU provides velocity in NED frame via Twist message
        if self.latest_twist is not None:
            # Twist linear components are in NED: x=North, y=East, z=Down
            gps_input.vel_n = self.latest_twist.linear.x  # North velocity (m/s)
            gps_input.vel_e = self.latest_twist.linear.y  # East velocity (m/s)
            gps_input.vel_d = self.latest_twist.linear.z  # Down velocity (m/s)
        else:
            # No velocity data yet
            gps_input.vel_n = 0.0
            gps_input.vel_e = 0.0
            gps_input.vel_d = 0.0
        
        # Accuracy estimates (set to max/unknown since we don't have these from NavSatFix)
        gps_input.speed_accuracy = 0.0  # Speed accuracy (m/s)
        gps_input.horiz_accuracy = 0.0  # Horizontal accuracy (m)
        gps_input.vert_accuracy = 0.0   # Vertical accuracy (m)
        
        # Use current time in microseconds
        gps_input.time_usec = int(time.time() * 1e6)
        
        # Ignore flags - only ignore accuracy metrics we don't have
        gps_input.ignore_flags = (
            GPSRAW.GPS_INPUT_IGNORE_FLAG_SPEED_ACCURACY |
            GPSRAW.GPS_INPUT_IGNORE_FLAG_HORIZ_ACCURACY |
            GPSRAW.GPS_INPUT_IGNORE_FLAG_VERT_ACCURACY
        )
        
        # GPS fix type (1 = No fix, 2 = 2D fix, 3 = 3D fix)
        # NavSatFix.status.status: -1 = No fix, 0 = Fix, 1 = SBAS fix, 2 = GBAS fix
        if msg.status.status == -1:
            gps_input.fix_type = 1  # No fix
        elif msg.status.status == 0:
            # Assume 3D fix if we have altitude data
            gps_input.fix_type = 3 if msg.altitude != 0.0 else 2
        else:
            gps_input.fix_type = 3  # SBAS or GBAS fix
        
        # Number of satellites
        gps_input.satellites_visible = msg.status.service  # service field contains satellite count
        
        # Publish the GPS input message
        self.gps_input_pub.publish(gps_input)
        
        self.get_logger().debug(
            f'GPS Data: Lat={msg.latitude:.6f}, Lon={msg.longitude:.6f}, '
            f'Alt={msg.altitude:.2f}m, Fix={gps_input.fix_type}, Sats={gps_input.satellites_visible}, '
            f'Vel=({gps_input.vel_n:.2f}, {gps_input.vel_e:.2f}, {gps_input.vel_d:.2f}) m/s'
        )

    def twist_callback(self, msg: Twist):
        """
        Callback function for incoming velocity data from the Advanced Navigation IMU.
        Stores the latest twist data to be used in GPS updates.
        """
        self.latest_twist = msg


def main(args=None):
    rclpy.init(args=args)
    node = GPSToArdupilot()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down GPS to ArduPilot node')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
