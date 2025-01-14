#!/usr/bin/python3
import os
from ament_index_python.packages import get_package_share_directory, get_package_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch.actions import OpaqueFunction
from launch.actions import SetLaunchConfiguration

import xacro

def generate_launch_description():

    use_sim_time     = LaunchConfiguration('use_sim_time', default='true')
    namespace_arg    = DeclareLaunchArgument('namespace', default_value=TextSubstitution(text='r0'))
    robot_arg        = DeclareLaunchArgument('robot',     default_value=TextSubstitution(text='pioneer3dx'))
    X_launch_arg     = DeclareLaunchArgument('X',         default_value=TextSubstitution(text='0.0'))
    Y_launch_arg     = DeclareLaunchArgument('Y',         default_value=TextSubstitution(text='0.0'))
    Theta_launch_arg = DeclareLaunchArgument('Theta',     default_value=TextSubstitution(text='0.0'))

    models_dir = get_package_share_directory('tuw_gazebo_models') + '/models'



    def create_robot_description(context): 
        xacro_file = os.path.join(get_package_directory('tuw_gazebo_models'), 'models', context.launch_configurations['robot'], 'main.xacro')    
        assert os.path.exists(xacro_file), "The main.xacro doesnt exist in "+str(xacro_file)
        robot_description_config = xacro.process_file(xacro_file, 
            mappings={  "namespace": context.launch_configurations['namespace'], 
                        "models_dir": models_dir})
        robot_desc = robot_description_config.toxml()
        return [SetLaunchConfiguration('robot_desc', robot_desc)]

    create_robot_description_arg = OpaqueFunction(function=create_robot_description)

    return LaunchDescription([
        namespace_arg,
        robot_arg,
        X_launch_arg,
        Y_launch_arg,
        Theta_launch_arg,
        create_robot_description_arg,
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        Node(package='tuw_gazebo_models', 
            name="publisher_robot", 
            executable='spawn_robot.py', 
            arguments=[LaunchConfiguration('robot_desc')],
            parameters=[{
                "X": LaunchConfiguration('X'),
                "Y": LaunchConfiguration('Y'),
                "Theta": LaunchConfiguration('Theta'),
                "namespace": LaunchConfiguration('namespace')}],
            output='screen'),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            namespace=[LaunchConfiguration('namespace')],
            parameters=[{
                "robot_description": LaunchConfiguration('robot_desc'),
                "namespace": LaunchConfiguration('namespace')}],
            output="screen"),
    ])
