# turtleism_cleaner
Implementation of turtleism clean in ROS 2. 

Steps to Run it. 
ROS 2 and Turtleism must be installed beforehand. 

1. Run the turtleism_node and turtleism_teleop_key node by following commands in different terminals. 

 ros2 run turtlesim turtlesim_node
 ros2 run turtlesim turtle_teleop_key

2. Clone the repository to your ROS 2 WS folder
3. Run the following command in the src forlder
colcon build --packages-select turtlesim_cleaner
4. To go to goal straightly use this command. 

ros2 run turtlesim_cleaner gotogoal_straight 1 1 1.57 0.1 0.01

Parameters explanition ^ first two params are "x" and "y", Third param is theta (where do you want to orient the turtle before moving it) 
fourth and fifth parameters are distance tolerance and angular torlerance respectivly. 



5. To go to goal in cicular motion, run the following command
ros2 run turtlesim_cleaner gotogoal 1 1 0.1
