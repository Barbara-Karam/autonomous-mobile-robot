cmake_minimum_required(VERSION 3.8)
project(custom_diff_drive)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(ros_ign_gazebo REQUIRED)
find_package(ros_ign_bridge REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(xacro REQUIRED)
find_package(ros_gz_bridge REQUIRED)

add_executable(custom_diff_drive_node src/custom_diff_drive_node.cpp)
ament_target_dependencies(custom_diff_drive_node rclcpp std_msgs geometry_msgs robot_state_publisher ros_ign_gazebo ros_ign_bridge nav_msgs tf2_msgs xacro ros_gz_bridge)


install(TARGETS
  custom_diff_drive_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY
  urdf
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY
  rviz
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY
  worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)
install(DIRECTORY
  maps/
  DESTINATION share/${PROJECT_NAME}/maps
)
ament_package()
