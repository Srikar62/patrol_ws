import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
import time

# Define your waypoints as (x, y) coordinates from your map
WAYPOINTS = [
    (1.0,  0.5),
    (2.0, -1.0),
    (0.5,  1.5),
    (-1.0, 0.5),
]

DOCK_POSITION = (0.0, 0.0)
BATTERY_DRAIN_PER_WAYPOINT = 10
LOW_BATTERY_THRESHOLD = 20

class PatrolNode(Node):
    def __init__(self):
        super().__init__('patrol_node')
        self.navigator = BasicNavigator()
        self.battery = 100.0
        self.state = 'PATROLLING'

        # Publisher so alert_node can also trigger RTB
        self.alert_sub = self.create_subscription(
            Bool, '/intruder_detected', self.alert_callback, 10)
        self.intruder_flag = False

    def alert_callback(self, msg):
        if msg.data:
            self.intruder_flag = True
            self.get_logger().warn('Intruder signal received — halting patrol!')

    def make_pose(self, x, y):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.w = 1.0
        return pose

    def go_to(self, x, y, label=''):
        goal = self.make_pose(x, y)
        self.navigator.goToPose(goal)
        while not self.navigator.isTaskComplete():
            if self.intruder_flag:
                self.navigator.cancelTask()
                self.get_logger().warn('Task cancelled — intruder alert!')
                return False
            time.sleep(0.5)
        self.get_logger().info(f'Reached {label} ({x}, {y})')
        return True

    def patrol(self):
        self.navigator.waitUntilNav2Active()
        self.get_logger().info('Nav2 active — starting patrol...')

        while rclpy.ok():
            if self.state == 'PATROLLING':
                for i, (x, y) in enumerate(WAYPOINTS):
                    self.battery -= BATTERY_DRAIN_PER_WAYPOINT
                    self.get_logger().info(f'Battery: {self.battery}%')

                    if self.battery <= LOW_BATTERY_THRESHOLD:
                        self.state = 'RETURN_TO_BASE'
                        break

                    if self.intruder_flag:
                        self.state = 'ALERT'
                        break

                    self.go_to(x, y, label=f'waypoint {i+1}')

            elif self.state == 'ALERT':
                self.get_logger().warn('STATE: ALERT — waiting 5s then resuming...')
                time.sleep(5)
                self.intruder_flag = False
                self.state = 'PATROLLING'

            elif self.state == 'RETURN_TO_BASE':
                self.get_logger().info('STATE: RETURN_TO_BASE')
                self.go_to(*DOCK_POSITION, label='dock')
                self.get_logger().info('Docked! Recharging...')
                time.sleep(5)  # simulate recharge
                self.battery = 100.0
                self.state = 'PATROLLING'

def main():
    rclpy.init()
    node = PatrolNode()
    node.patrol()

if __name__ == '__main__':
    main()
