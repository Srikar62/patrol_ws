from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sensing_node',
            executable='lowlight_node',
            name='lowlight_node',
            output='screen'
        ),
        Node(
            package='navigation_fsm',
            executable='patrol_node',
            name='patrol_node',
            output='screen'
        ),
        Node(
            package='alert_system',
            executable='alert_node',
            name='alert_node',
            output='screen'
        ),
    ])
    
