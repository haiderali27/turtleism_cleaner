#!/usr/bin/env python
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
import sys
PI = 3.1415926535897

class rotate(Node):

    def __init__(self, speed, angle, clockWise):
        # Initialize the node
        super().__init__('RotateNode')
        # Initialize the publisher
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.rotateAroundWithParams(speed=speed, angle=angle, clockwise=True))

    def rotateAround(self):
        # Receiveing the user's input
        speed=50.0
        angle=2.0
        clockwise=True
        self.get_logger().info(f'Lets rotate your robot with speed: ${speed}, angle: ${angle}, clockwise: ${clockwise} ')
        #speed = input("Input your speed (degrees/sec):")
        #angle = input("Type your distance (degrees):")
        #clockwise = input("Clowkise?: ") #True or false
        # 
        #Converting from angles to radians
        angular_speed = speed*2*PI/360
        relative_angle = angle*2*PI/360
        vel_msg = Twist()
        #We wont use linear components
        vel_msg.linear.x=1.0
        vel_msg.linear.y=0.0
        vel_msg.linear.z=0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0

        # Checking if our movement is CW or CCW
        if clockwise:
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)
        # Setting the current time for distance calculus
        t0 = self.get_clock().now().to_msg()._sec
        current_angle = 0.0

        while(current_angle < relative_angle):
            self.publisher_.publish(vel_msg)
            t1 = self.get_clock().now().to_msg()._sec
            current_angle = angular_speed*(t1-t0)


        #Forcing our robot to stop
        vel_msg.angular.z = 0.0
        self.publisher_.publish(vel_msg)

      

    def rotateAroundWithParams(self, speed, angle, clockwise):
        # Receiveing the user's input
        self.get_logger().info(f'Lets rotate your robot with speed: ${speed}, angle: ${angle}, clockwise: ${clockwise} ')
        #speed = input("Input your speed (degrees/sec):")
        #angle = input("Type your distance (degrees):")
        #clockwise = input("Clowkise?: ") #True or false
        # 
        #Converting from angles to radians
        angular_speed = speed*2*PI/360
        relative_angle = angle*2*PI/360
        vel_msg = Twist()
        #We wont use linear components
        vel_msg.linear.x=1.0
        vel_msg.linear.y=0.0
        vel_msg.linear.z=0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0

        # Checking if our movement is CW or CCW
        if clockwise:
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)
        # Setting the current time for distance calculus
        t0 = self.get_clock().now().to_msg()._sec
        current_angle = 0.0

        while(current_angle < relative_angle):
            self.publisher_.publish(vel_msg)
            t1 = self.get_clock().now().to_msg()._sec
            current_angle = angular_speed*(t1-t0)


        #Forcing our robot to stop
        vel_msg.angular.z = 0.0
        self.publisher_.publish(vel_msg)

def main(args=None):
    rclpy.init(args=args)
    
    # we are using try-except tools to  catch keyboard interrupt
    try:
        # create an object for rotate class
        cmd_publisher = rotate(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
        #cmd_publisher.rotateAround(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[2]))
        # continue untill interrupted
        #rclpy.spin(cmd_publisher)
        
    except KeyboardInterrupt:
        # execute shutdown function
        cmd_publisher.stop_turtlebot()
        # clear the node
        cmd_publisher.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()

