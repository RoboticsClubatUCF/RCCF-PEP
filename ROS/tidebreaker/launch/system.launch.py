from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource#, FrontendLaunchDescriptionSource
#from launch_ros.actions import ComposableNodeContainer, Node
#from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    vesc_launch = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=str(get_package_share_path("vesc_driver") / "launch" / "vesc_driver_node.launch.py")
        ),
    )

    adnav_launch = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=str(get_package_share_path("adnav_launch") / "launch" / "adnav_serial.launch.py")
        ),
    )   

    send_gps_to_ardupilot_launch = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=str(get_package_share_path("tidebreaker") / "launch" / "send_gps_to_ardupilot.launch.py")
        ),
    ) 

    return LaunchDescription(
        [
            vesc_launch,
            adnav_launch,
            send_gps_to_ardupilot_launch,
        ]
    )

