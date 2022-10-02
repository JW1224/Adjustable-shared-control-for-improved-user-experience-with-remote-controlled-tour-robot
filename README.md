# Adjustable shared control for improved user experience with remote controlled tour robot 

## Required to run:  
-MATLAB 2022a  
-Python 3.9  
-Virtual Machine IP address running Gazebo sim with turtlebot (noetic or foxy)
-Xbox controller  

## Setup
### Step 1: 
Install Required Python Modules
```
$ python -m pip install inputs
$ python -m pip install matlabengine==9.12
```
### Step 2:
Install MATLAB 2022a with the following toolboxes:  
-Navigation Toolbox   
-ROS Toolbox  
-Robotics System Toolbox   
-Image Processing Toolbox   

### Step 3:
Install Virtual Machine, a suitable one can be downloaded from the following link run using VMware.
```
https://uk.mathworks.com/support/product/robotics/ros2-vm-installation-instructions-v7.html
```

### Step 4:  
Before running, in the virtual machine open the terminal and run the following command:  
```
nano /home/user/start-gazebo-office.sh
```
Then change the turtle bot model to waffle_pi, the code can then be run.

If you are using a different map you need to follow the instuctions below.  

To set up the environment a top down image of the area you intend to use needs to be made (like MapOffice.png) that is 10 pixels for every meter in dimensions. Then in the connectRob.m function the name of the image should replace the MapOffice in line 6 and the coordinates of the bottom left corner should replace the ones in line 9.
In the Test algorithm file the rooms in you environment should have their top left and bottom right coordinates added to rooms, and the coordinates of the points of interest in the rooms should be added to POIs. Also make sure to change the robot to waffle_pi as explained before.
