from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
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

    robot_desc = ParameterValue(
        Command([
            'xacro ', LaunchConfiguration('model')
        ])
    )

    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': True,
            "robot_description": robot_desc
        }]
    )

    joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    return LaunchDescription([
        declare_model,
        robot_state_publisher_cmd,
        joint_state_publisher_cmd
    ])