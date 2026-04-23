import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from std_msgs.msg import Bool

class LowLightNode(Node):
    def __init__(self):
        super().__init__('lowlight_node')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.callback, 10)
        self.pub_enhanced = self.create_publisher(
            Image, '/camera/enhanced', 10)
        self.pub_alert = self.create_publisher(
            Bool, '/intruder_detected', 10)
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=False)
        self.get_logger().info('LowLight node started!')

    def callback(self, msg):
        # Convert ROS image to OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        # --- CLAHE Low-light Enhancement ---
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)

        # Publish enhanced image
        self.pub_enhanced.publish(
            self.bridge.cv2_to_imgmsg(enhanced, 'bgr8'))

        # --- MOG2 Background Subtraction for Intruder Detection ---
        fg_mask = self.bg_subtractor.apply(enhanced)

        # Morphological cleanup to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        motion_pixels = cv2.countNonZero(fg_mask)
        self.get_logger().info(f'Motion pixels: {motion_pixels}')

        if motion_pixels > 500:
            self.get_logger().warn('🚨 Intruder detected!')
            self.pub_alert.publish(Bool(data=True))
        else:
            self.pub_alert.publish(Bool(data=False))

def main():
    rclpy.init()
    node = LowLightNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
