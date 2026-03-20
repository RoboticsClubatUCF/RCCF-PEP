import launch
import launch.actions
import launch.substitutions
import launch_ros.actions
#from launch.actions import DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='tidebreaker',
            executable='send_gps_to_ardupilot',
            name='send_gps_to_ardupilot_node',
            output='log',
        ),
    ])
