#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import SetEnvironmentVariable


def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_tuw_gazebo = get_package_share_directory('tuw_gazebo')
    pkg_tuw_gazebo_models = get_package_share_directory('tuw_gazebo_models')
    pkg_tuw_gazebo_plugins = get_package_share_directory('tuw_gazebo_plugins')


    if 'GAZEBO_MODEL_PATH' in os.environ:
        model_path =  os.environ['GAZEBO_MODEL_PATH'] + ':' + pkg_tuw_gazebo_models + '/models'
    else:
        model_path =  pkg_tuw_gazebo_models + '/models'

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )    


    return LaunchDescription([
        SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=model_path),
        DeclareLaunchArgument(
          'world',
          default_value=[os.path.join(pkg_tuw_gazebo, 'worlds', 'roblab.world'), ''],
          description='SDF world file'),
        DeclareLaunchArgument(
          'verbose',
          default_value='true',
          description='SDF world file'),
        gazebo
    ])