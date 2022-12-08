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
        self.rate = self.create_rate(2)
        timer_period = 0.5  # seconds
        # Initialize a timer that excutes call back function every 0.5 seconds
        self.timer = self.create_timer(timer_period, self.move2goal)
        self.pose = Pose()
        self.flag= False

    #Callback function implementing the pose value received
    def callback(self, data :Pose):
        self.pose.x= data.x
        self.pose.y = data.y
        self.pose.theta = data.theta
        #self.get_logger().info(f'data: ${data}')
        #self.pose.x = round(self.pose.x, 4)
        #self.pose.y = round(self.pose.y, 4)

    def get_distance(self, goal_x, goal_y):
        distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
        return distance

    def move2goal(self):
        self.get_logger().info(f'X:${float(sys.argv[1])}, Y:${float(sys.argv[2])}, distance_tolerance:${float(sys.argv[3])}')
        goal_pose = Pose()
        goal_pose.x = float(sys.argv[1]) 
        goal_pose.y =  float(sys.argv[2])
        distance_tolerance = float(sys.argv[3])

        vel_msg = Twist()


        if sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) >= distance_tolerance:
            #Porportional Controller
            #linear velocity in the x-axis:
            dist = sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
            dist_ = self.get_distance(goal_pose.x, goal_pose.y)
            self.get_logger().info(f'dist_: ${dist_} ,dis ${dist}, distance_tolerance:${float(sys.argv[3])} pose: ${self.pose}, goal:${goal_pose}')

            vel_msg.linear.x = 1.5 * sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0

            #angular velocity in the z-axis:
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = 4 * (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x) - self.pose.theta)

            #Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            
            self.rate.sleep()
        #Stopping our robot after the movement is over
        else :
            vel_msg.linear.x = 0.0
            vel_msg.angular.z =0.0        
            self.velocity_publisher.publish(vel_msg)
            self.get_logger().info(f'stopping')
            quit()

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
