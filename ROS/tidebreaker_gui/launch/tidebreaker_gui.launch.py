#!/usr/bin/env python3
"""
Launch file for the Tidebreaker GUI.

This launch file starts the Tidebreaker GUI dashboard.
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """Generate the launch description for the Tidebreaker GUI."""
    
    # Declare launch arguments
    gui_node_name = DeclareLaunchArgument(
        'node_name',
        default_value='tidebreaker_gui',
        description='Name of the GUI node'
    )
    
    # Create the ROS2 node for the GUI
    gui_node = Node(
        package='tidebreaker_gui',
        executable='tidebreaker_gui',
        name=LaunchConfiguration('node_name'),
        output='screen',
        emulate_tty=True,
    )
    
    return LaunchDescription([
        gui_node_name,
        gui_node,
    ])
