#!/usr/bin/env python
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
import sys

# "move" class inherits from the base class "Node"
class move(Node):

    def __init__(self):
        # Initialize the node
        super().__init__('MoveNode')
        # Initialize the publisher
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        #timer_period = 0.5  # seconds
        # Initialize a timer that excutes call back function every 0.5 seconds
        #self.timer = self.create_timer(timer_period, self.move_callback)
    
        
    def timer_callback(self):
        # Create an object of msg type Twist() 
        # and define linear velocity and angular velocity
        move_cmd = Twist()
        move_cmd.linear.x = 0.2
        move_cmd.angular.z = 0.0
        #publish  the velcity command
        self.publisher_.publish(move_cmd)
        #log details of the current phase of execution
        self.get_logger().info('Publishing cmd_vel')
        
    def stop_turtlebot(self):
        # define what happens when program is interrupted
        # log that turtlebot is being stopped
        self.get_logger().info('stopping turtlebot')
        # publishing an empty Twist() command sets all velocity components to zero
        # Otherwise turtlebot keeps moving even if command is stopped
        self.publisher_.publish(Twist())
        
    

    def move_callback(self, speed, distance, isForward):
    
        vel_msg = Twist()
    
        #Receiveing the user's input
        self.get_logger().info(f'Setting speed, distance and direction ${speed}, ${distance}, ${isForward}')
    
    
        #Checking if the movement is forward or backwards
        if(isForward):
            vel_msg.linear.x = abs(speed)
        else:
            vel_msg.linear.x = -abs(speed)
        #Since we are moving just in x-axis
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0
        self.get_logger().info(f'msg: ${vel_msg}')
   
        t0 = float(self.get_clock().now().to_msg()._sec)
        current_distance = 0
        #self.get_logger().info(f'current_distance: ${current_distance}')


        #Loop to move the turtle in an specified distance
        while(current_distance < distance):
            #self.get_logger().info(f'current_distance: ${current_distance}')
            #Publish the velocity
            self.publisher_.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=float(self.get_clock().now().to_msg()._sec)
            #Calculates distancePoseStamped
            current_distance= speed*(t1-t0)
        
        #After the loop, stops the robot
        vel_msg.linear.x = 0.0
        #Force the robot to stop
        self.publisher_.publish(vel_msg)




def main(args=None):
    rclpy.init(args=args)
    
    # we are using try-except tools to  catch keyboard interrupt
    try:
        # create an object for move class
        cmd_publisher = move()
        cmd_publisher.move_callback(float(sys.argv[1]), float(sys.argv[2]), bool(sys.argv[3]))
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


