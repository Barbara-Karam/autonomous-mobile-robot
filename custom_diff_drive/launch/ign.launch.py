import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('custom_diff_drive')
    xacro_file = os.path.join(pkg_share, 'urdf', 'lab.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}
    config_file = os.path.join(pkg_share, 'config', 'ekf_parameters.yaml')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'slam.rviz')
    slam_config_file = os.path.join(pkg_share, 'config', 'mapper_params_online_async.yaml')
    world_file = os.path.join(pkg_share, 'worlds', 'room.sdf')


    ekf_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[
            config_file,
            {'use_sim_time': True}
        ]
    )


    set_ign_plugin_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_SYSTEM_PLUGIN_PATH',
        value='/opt/ros/humble/lib'
    )

    set_ign_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value='/opt/ros/humble/share:' + os.path.join(pkg_share, 'worlds')
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_ign_gazebo'),
                'launch', 'ign_gazebo.launch.py'
            )
        ]),
        launch_arguments={'ign_args': '-r room.sdf'}.items()
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description
                     ,{'use_sim_time': True}
                     ]
    )

    custom_diff_drive_node = Node(
        package='custom_diff_drive',
        executable='custom_diff_drive_node',
        name='custom_diff_drive_node',
        output='screen',
        parameters=[{
            'use_sim_time': True
        }]
    )

    spawn_robot = Node(
        package='ros_ign_gazebo',
        executable='create',
        arguments=[
            '-name', 'mobile_robot',
            '-topic', '/robot_description',
            '-z', '0.9'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/mobile_robot/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/model/mobile_robot/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU',
            '/lidar@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
        ],
        remappings=[
            ('/lidar', '/scan'),
        ],
        output='screen'
    )
    clock_bridge = Node(
       package='ros_gz_bridge',
       executable='parameter_bridge',
       arguments=[
           '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
       ],
       output='screen'
    )
    teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        output='screen',
        emulate_tty=True,
        remappings=[('cmd_vel', '/cmd_vel')],
        prefix='xterm -e'
    )
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('slam_toolbox'),
                'launch', 'online_async_launch.py'
            )
        ]),
        launch_arguments={
            'slam_params_file': slam_config_file,
            'use_sim_time': 'true'
        }.items()
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': True}]
    )

    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--roll', '0', '--pitch', '0', '--yaw', '0',
            '--frame-id', 'lidar_link',
            '--child-frame-id', 'mobile_robot/base_link/gpu_lidar'
        ]
    )


    return LaunchDescription([
        set_ign_plugin_path,
        set_ign_resource_path,
        lidar_tf,
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        custom_diff_drive_node,
        bridge,
        clock_bridge,
        ekf_node,
        teleop,
        # slam,
        rviz,
        TimerAction(period=3.0, actions=[spawn_robot])
    ])
