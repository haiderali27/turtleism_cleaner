#!/usr/bin/env python
import rclpy
from rclpy.node import Node
import sys
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
import time
class turtlebot(Node):

    def __init__(self):
        #Creating our node,publisher and subscriber
        super().__init__('turtlebot_controller')
        self.velocity_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose',self.callback, 10)
        timer_period = 0.5  # seconds
        # Initialize a timer that excutes call back function every 0.5 seconds
        self.timer = self.create_timer(timer_period, self.movetogoal)
        self.pose = Pose()
        self.flag= False

    #Callback function implementing the pose value received
    def callback(self, data :Pose):
        self.pose.x= data.x
        self.pose.y = data.y
        self.pose.theta = data.theta

    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
    def linear_vel(self, goal_pose, constant=2):
        return constant*self.euclidean_distance(goal_pose)
    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
    def angular_vel(self, goal_pose, constant=2):
        return constant*(self.steering_angle(goal_pose) - self.pose.theta)
    
    def movetogoal(self):
        x_ = float(sys.argv[1])
        y_ = float(sys.argv[2])
        theta = float(sys.argv[3])
        dis_tol = float(sys.argv[4])
        ang_tol = float(sys.argv[5])
        self.get_logger().info(f'X:${x_}, Y:${y_}, theta: ${theta},distance_tolerance:${dis_tol}, angular_tolerance: ${ang_tol}')
        goal_pose = Pose()
        goal_pose.x = x_ 
        goal_pose.y =  y_
        goal_pose.theta =  theta
        distance_tolerance = dis_tol
        angular_tolerance = ang_tol
        vel_msg = Twist()
        if abs(self.steering_angle(goal_pose) - self.pose.theta) > angular_tolerance:
            self.get_logger().info("1")
            vel_msg.linear.x=0.0
            vel_msg.angular.z = self.angular_vel(goal_pose)
        else:
            self.get_logger().info("2")
            vel_msg.angular.z = 0.0
            if self.euclidean_distance(goal_pose)>=distance_tolerance:
                self.get_logger().info("2_1")
                vel_msg.linear.x = self.linear_vel(goal_pose)
            else: 
                self.get_logger().info("2_2")
                vel_msg.linear.x = 0.0
                self.flag=True
        if self.flag:
            vel_msg.angular.z = goal_pose.theta - self.pose.theta
            if abs(goal_pose.theta - self.pose.theta) <=angular_tolerance:
                quit()
        
        self.get_logger().info(f'vel_msg: ${vel_msg}, ${self.euclidean_distance(goal_pose)}, ${self.linear_vel(goal_pose)}')

        self.velocity_publisher.publish(vel_msg)




def main(args=None):
    
    # we are using try-except tools to  catch keyboard interrupt
    try:
        rclpy.init(args=args)
        # create an object for turtlebot class
        x = turtlebot()
        rclpy.spin(x)
        #x.move2goal(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
        
    
        
    except KeyboardInterrupt:
        # execute shutdown function
        x.stop_turtlebot()
        # clear the node
        x.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()
