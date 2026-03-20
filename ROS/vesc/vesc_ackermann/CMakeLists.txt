cmake_minimum_required(VERSION 3.5)
project(vesc_ackermann)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(ackermann_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(vesc_msgs REQUIRED)

###########
## Build ##
###########

# node executable
add_executable(vesc_to_odom_node src/vesc_to_odom_node.cpp
                                 src/vesc_to_odom.cpp)
target_include_directories(vesc_to_odom_node PRIVATE include)
ament_target_dependencies(vesc_to_odom_node
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  tf2
  vesc_msgs
)

add_executable(ackermann_to_vesc_node src/ackermann_to_vesc_node.cpp
                                      src/ackermann_to_vesc.cpp)
target_include_directories(ackermann_to_vesc_node PRIVATE include)
ament_target_dependencies(ackermann_to_vesc_node
  rclcpp
  std_msgs
  ackermann_msgs
  vesc_msgs
)

# nodelet library
add_library(vesc_ackermann_nodelet src/ackermann_to_vesc_nodelet.cpp
                                   src/ackermann_to_vesc.cpp
                                   src/vesc_to_odom_nodelet.cpp
                                   src/vesc_to_odom.cpp)
target_include_directories(vesc_ackermann_nodelet PRIVATE include)
ament_target_dependencies(vesc_ackermann_nodelet
  rclcpp_components
  pluginlib
  std_msgs
  geometry_msgs
  nav_msgs
  ackermann_msgs
  tf2
  vesc_msgs
)
rclcpp_components_register_node(vesc_ackermann_nodelet PLUGIN "vesc_ackermann::AckermannToVescNodelet" EXECUTABLE ackermann_to_vesc_nodelet_node)
rclcpp_components_register_node(vesc_ackermann_nodelet PLUGIN "vesc_ackermann::VescToOdomNodelet" EXECUTABLE vesc_to_odom_nodelet_node)

#############
## Install ##
#############

install(TARGETS vesc_to_odom_node ackermann_to_vesc_node
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS vesc_ackermann_nodelet
  LIBRARY DESTINATION lib
)

install(DIRECTORY include/${PROJECT_NAME}/
        DESTINATION include/${PROJECT_NAME}/)
install(FILES vesc_ackermann_nodelet.xml
        DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY launch/
        DESTINATION share/${PROJECT_NAME}/launch)

ament_package()
