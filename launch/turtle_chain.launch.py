#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    num_turtles_arg = DeclareLaunchArgument(
        'num_turtles',
        default_value='4',
        description='Количество черепах в цепочке (включая turtle1)'
    )
    
    spawn_turtlesim_arg = DeclareLaunchArgument(
        'spawn_turtlesim',
        default_value='true',
        description='Запускать ли turtlesim_node'
    )
    
    num_turtles = LaunchConfiguration('num_turtles')
    spawn_turtlesim = LaunchConfiguration('spawn_turtlesim')
    
    # Узел симулятора
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen'
    )
    
    # Генерация нод-последователей
    follower_nodes = []
    base_offset = 1.5
    
    # Цепочка: turtle2 -> turtle1, turtle3 -> turtle2, ...
    for i in range(2, 10):
        spawn_x = 5.0 + (i - 2) * base_offset
        spawn_y = 5.0 + (i - 2) * base_offset
        if spawn_x > 10.0 or spawn_y > 10.0:
            break
        
        follower = Node(
            package='hello_turtle',  # ✅ Имя пакета из package.xml
            executable='turtle_cmd',  # ✅ Имя из entry_points в setup.py
            name=f'turtle_cmd_{i}',
            output='screen',
            parameters=[{
                'name': f'turtle{i}',
                'target': f'turtle{i-1}',
                'spawn_x': float(spawn_x),
                'spawn_y': float(spawn_y),
                'spawn_theta': 0.0,
                'speed': 1.5,
                'tolerance': 0.5
            }],
            emulate_tty=True
        )
        # Задержка для стабильного спавна
        follower_nodes.append(TimerAction(period=float(i - 2) * 0.5, actions=[follower]))
    
    return LaunchDescription([
        num_turtles_arg,
        spawn_turtlesim_arg,
        turtlesim_node,
        *follower_nodes,
    ])