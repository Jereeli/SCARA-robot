import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState # The datatype used to communicate with joint_publisher
from scara_interfaces.srv import SetJointValues

class JointConfigurationServer(Node):
    def __init__(self):
        super().__init__('JointConfiguration') # Inhereit the construct of class Node
        # Create a publisher that publishes JointState datatype data into topic /joint_states.
        # joint_publisher reads the topic /joint_states
        
        self.joint_publisher = self.create_publisher(JointState, "/joint_states", 10)
        self.service = self.create_service(SetJointValues, "/set_joint_values", self.set_joint_values_callback)

        # The joint names
        self.joint_names = [
            'base_to_link1',
            'link2_to_link3',
            'link4_to_link5',
            'link5_to_link6',
        ]

    def set_joint_values_callback(self, request, response):
        # Takes the joint values as a list as input. Checks if they are within the
        # limits of the joints, then returns a response wheter the operation
        # was succesfull or not.

        # Convert the joint angles into a python list
        joint_angles = list(request.joint_angles)

        if len(joint_angles) != 4:
            response.success=False
            response.info="Please provide the value of each joint (4)"
            return response

        # Save the joint values
        r1 = joint_angles[0]
        r2 = joint_angles[1]
        r3 = joint_angles[2]
        d1 = joint_angles[3]

        revolute_joints = [r1, r2, r3]

        # Checks that every given value is in the limits
        if not all(-3.14 <= angle <= 3.14 for angle in revolute_joints) or not (-0.23 <= d1 <= 0.065):
            response.success = False
            response.info = "Some of the given joint is out of limits! (Limits for revolute joints" \
            "are -3.14 and 3.14, and prismatic joint -0.23 and 0.065)"
            return response
        
        else:
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg() # JointState needs the current time
            msg.name = self.joint_names # JointState requires the joint names
            msg.position = joint_angles # The joint angles

            self.joint_publisher.publish(msg) # Publish the message

            response.success = True
            response.info = "The joints published successfully"
            return response



def main(args=None):
    rclpy.init(args=args) # initialize ROS2 communications
    node = JointConfigurationServer() # Create an object node
    rclpy.spin(node) # Loop the node
    rclpy.shutdown() # shutdown ros2 communications

if __name__ == '__main__':
    main()