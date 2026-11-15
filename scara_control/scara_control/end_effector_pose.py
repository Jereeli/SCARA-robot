import rclpy
from rclpy.node import Node
import tf2_ros
from scara_interfaces.srv import GetTcpPose
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import geometry_msgs


class GetTcp(Node):
    def __init__(self):
        super().__init__('TcpPose')


        self.buffer = Buffer() # Buffer used for transform listener
        self.listener = TransformListener(self.buffer, self)
        # Create a service
        self.service = self.create_service(GetTcpPose, '/get_tcp', self.get_tcp_callback)


    def get_tcp_callback(self, request, response):
        # Try to get the transform
        try:

            trans = self.buffer.lookup_transform(
                'base_link', # Base frame name (from)
                'TCP', # TCP frame name (to)
                rclpy.time.Time()
            )

            # Since the interface GetTcpPose has geometry_msgs datatype:
            response.position.position.x = trans.transform.translation.x
            response.position.position.y = trans.transform.translation.y
            response.position.position.z = trans.transform.translation.z
            response.position.orientation = trans.transform.rotation

            response.success = True

        except Exception as e:
            self.get_logger().info(f"Error {e}")

            response.success = False


        return response

def main(args=None):
    rclpy.init(args=args)
    node = GetTcp()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
