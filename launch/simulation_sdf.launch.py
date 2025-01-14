from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import Command
from launch.conditions import IfCondition

from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():

    declare_model = DeclareLaunchArgument(
        name='model',
        default_value=PathJoinSubstitution([
            FindPackageShare('realsense_ros_gazebo'),
            'sdf',
            'realsense_d435i',
            'realsense_d435i.sdf'
        ])
    )

    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true'
    )

    killall_gzserver_cmd = ExecuteProcess(
        cmd=['killall','-q', 'gzserver'],
        output='screen'
    )
    
    killall_gzclient_cmd = ExecuteProcess(
        cmd=['killall','-q', 'gzclient'],
        output='screen'
    )

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("gazebo_ros"),
                'launch',
                'gzserver.launch.py'
            ])
        )
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("gazebo_ros"),
                'launch',
                'gzclient.launch.py'
            ])
        )
    )

    joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    spawn_entity_cmd = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=[
            '-file', LaunchConfiguration('model'),
            '-entity', 'realsense_camera',
            '-x', '0',
            '-y', '0',
            '-z', '1',
            '-R', '1.57',
            '-P', '0',
            '-Y', '1.57',
        ],
        output='screen'
    )

    return LaunchDescription([
        declare_model,
        declare_use_sim_time,
        killall_gzserver_cmd,
        killall_gzclient_cmd,
        gzserver_cmd,
        gzclient_cmd,
        joint_state_publisher_cmd,
        spawn_entity_cmd
    ])