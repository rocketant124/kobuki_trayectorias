import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class MoverDistancia(Node):
    def __init__(self):
        super().__init__('mover_distancia')
        self.pub = self.create_publisher(Twist, '/commands/velocity', 10)
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.x_inicio = None
        self.y_inicio = None
        self.distancia_objetivo = 1.0  # metros
        self.get_logger().info(f'Avanzando {self.distancia_objetivo} metros...')

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        if self.x_inicio is None:
            self.x_inicio = x
            self.y_inicio = y

        distancia = math.sqrt((x - self.x_inicio)**2 + (y - self.y_inicio)**2)

        cmd = Twist()
        if distancia < self.distancia_objetivo:
            cmd.linear.x = 0.15
            self.get_logger().info(f'Distancia recorrida: {distancia:.3f}m')
        else:
            cmd.linear.x = 0.0
            self.pub.publish(cmd)
            self.get_logger().info('¡Objetivo alcanzado!')
            rclpy.shutdown()
            return

        self.pub.publish(cmd)

def main():
    rclpy.init()
    node = MoverDistancia()
    rclpy.spin(node)

if __name__ == '__main__':
    main()

