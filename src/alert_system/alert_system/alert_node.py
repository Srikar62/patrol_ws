import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from datetime import datetime

class AlertNode(Node):
    def __init__(self):
        super().__init__('alert_node')
        self.sub = self.create_subscription(
            Bool, '/intruder_detected', self.handle_alert, 10)
        self.pub = self.create_publisher(
            String, '/alert_status', 10)
        self.log_file = open('/tmp/patrol_alerts.log', 'a')
        self.alert_cooldown = False
        self.get_logger().info('Alert node started!')

    def handle_alert(self, msg):
        if msg.data and not self.alert_cooldown:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            alert_msg = f'[{timestamp}] ALERT: Intruder detected!'

            # Log to file
            self.log_file.write(alert_msg + '\n')
            self.log_file.flush()

            # Publish to ROS topic
            ros_msg = String()
            ros_msg.data = alert_msg
            self.pub.publish(ros_msg)

            self.get_logger().error(alert_msg)
            self.alert_cooldown = True

        elif not msg.data:
            self.alert_cooldown = False

def main():
    rclpy.init()
    node = AlertNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
