#launch ign then amcl then nav2
import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription#, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    navigation_pkg = get_package_share_directory("custom_diff_drive")

    map_yaml_file = os.path.join(
            navigation_pkg,
            "maps",
            "my_map5.yaml"
        )

    nav2_params = os.path.join(
        get_package_share_directory('custom_diff_drive'),
        'config', 'nav2_params.yaml'
    )

    nav2 = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(
            get_package_share_directory('nav2_bringup'),
            'launch', 'navigation_launch.py'
        )
    ]),
    launch_arguments={
        'use_sim_time': 'true',
        'params_file': nav2_params,
        'cmd_vel_topic': '/cmd_vel_nav',
    }.items()
    )
    
    return LaunchDescription([
        nav2
    ])
