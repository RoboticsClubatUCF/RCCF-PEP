cmake_minimum_required(VERSION 3.5)
project(vesc_driver)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(serial REQUIRED)
find_package(std_msgs REQUIRED)
find_package(vesc_msgs REQUIRED)

###########
## Build ##
###########

# node executable
add_executable(vesc_driver_node src/vesc_driver_node.cpp
                                src/vesc_driver.cpp
                                src/vesc_interface.cpp
                                src/vesc_packet.cpp
                                src/vesc_packet_factory.cpp)
target_include_directories(vesc_driver_node PRIVATE include)
ament_target_dependencies(vesc_driver_node
  rclcpp
  std_msgs
  vesc_msgs
  serial
)

# nodelet library
add_library(vesc_driver_nodelet src/vesc_driver_nodelet.cpp
                                src/vesc_driver.cpp
                                src/vesc_interface.cpp
                                src/vesc_packet.cpp
                                src/vesc_packet_factory.cpp)
target_include_directories(vesc_driver_nodelet PRIVATE include)
ament_target_dependencies(vesc_driver_nodelet
  rclcpp_components
  pluginlib
  std_msgs
  vesc_msgs
  serial
)
rclcpp_components_register_node(vesc_driver_nodelet PLUGIN "vesc_driver::VescDriverNodelet" EXECUTABLE vesc_driver_nodelet_node)

#############
## Install ##
#############

install(TARGETS vesc_driver_node
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS vesc_driver_nodelet
  LIBRARY DESTINATION lib
)

install(DIRECTORY include/${PROJECT_NAME}/
        DESTINATION include/${PROJECT_NAME}/)
install(FILES vesc_driver_nodelet.xml
        DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY launch/
        DESTINATION share/${PROJECT_NAME}/launch)

ament_package()
