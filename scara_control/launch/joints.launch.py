from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    
    joint_configuration = Node(
        package="scara_control",
        executable="joint_configuration",
    )

    end_effector_pose = Node(
        package="scara_control",
        executable="end_effector_pose",
    )

    ld.add_action(joint_configuration)
    ld.add_action(end_effector_pose)

    return ld