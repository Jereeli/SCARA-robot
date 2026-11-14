import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    ld = LaunchDescription()
    # Filepath for xacro-files
    robot_xacro_filepath = os.path.join(get_package_share_directory('scara_description'), 'urdf',
                                         'scara_robot_assembly.urdf.xacro')
    # Process the xacro file into a format python supports
    robot_description = xacro.process_file(robot_xacro_filepath).toxml()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{'robot_description': robot_description}],
    )

    robot_joint_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    rviz_filepath = os.path.join(get_package_share_directory('scara_description'), 'rviz', 'visualize_robot.rviz')

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['--display-config', rviz_filepath],
        )

    ld.add_action(robot_state_publisher)
    ld.add_action(robot_joint_publisher_gui)
    ld.add_action(rviz)

    return ld