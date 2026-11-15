import rclpy
import sys
from rclpy.node import Node
from sensor_msgs.msg import JointState 
from scara_interfaces.srv import SetJointValues
from scara_interfaces.srv import GetTcpPose
import time

class client(Node):
    def __init__(self):
        super().__init__('Client')
        # Create a client
        self.client_joint = self.create_client(SetJointValues, '/set_joint_values')
        self.client_tcp = self.create_client(GetTcpPose, '/get_tcp')
        self.request_joint = SetJointValues.Request() # Create an empty request
        self.request_tcp = GetTcpPose.Request()

    def call_joint_configuration(self, values):
        # Takes the joint values and sets them to the request
        self.request_joint.joint_angles = values

        while not self.client_joint.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service")

        # Send a request and save it as a Future object
        future = self.client_joint.call_async(self.request_joint)

        # Spin the node until response is received
        rclpy.spin_until_future_complete(self, future)

        return future.result()


    def call_end_effector_pose(self):
        while not self.client_tcp.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service")

        future = self.client_tcp.call_async(self.request_tcp)

        # Spin the node
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    node = client()

    # Extract the user input
    user_input_raw = rclpy.utilities.remove_ros_args(sys.argv)[1:]
    user_input = [float(x) for x in user_input_raw] # Match with the interface datatype


    response_joint = node.call_joint_configuration(user_input)
    # If the joints were given succesfully call the end effector pose service:
    time.sleep(0.2) # It takes time to calculate the TF
    if response_joint.success:
        response_tcp = node.call_end_effector_pose()
        if response_tcp.success:
            node.get_logger().info(f"End-effector orientation (quaternion): {response_tcp.position}")
    else:
        node.get_logger().warn(response_joint.info)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
