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
            'urdf',
            'test.xacro'
        ])
    )

    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true'
    )

    robot_desc = ParameterValue(
        Command([
            'xacro ', LaunchConfiguration('model')
        ])
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

    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': robot_desc
        }]
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
            '-topic', 'robot_description',
            '-entity', 'realsense_camera'
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
        robot_state_publisher_cmd,
        joint_state_publisher_cmd,
        spawn_entity_cmd
    ])