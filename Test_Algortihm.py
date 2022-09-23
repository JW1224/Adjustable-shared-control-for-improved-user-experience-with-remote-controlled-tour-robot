from asyncio import events
from inputs import get_gamepad
import inputs
import math
import matlab.engine
import time
import threading
from time import sleep

class XboxController(object):     #Xbox Controller class stores button states
    joyMax = math.pow(2, 15)      #MAximum joystick value

    def __init__(self):

        self.LJY = 0
        self.LJX = 0
        self.RJY = 0
        self.RJX = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0

        self.Start = 0


        self.updateThread = threading.Thread(target=self.updateC, args=())         #Creates Daemon thread to update class attributes
        self.updateThread.daemon = True
        self.updateThread.start()

    def updateC(self):
        while True:
            events = get_gamepad()              #Checks for events and updates the correct button based on the event
            for event in events:
                if event.code == 'ABS_Y':
                    self.LJY = event.state / XboxController.joyMax 
                elif event.code == 'ABS_X':
                    self.LJX = event.state / XboxController.joyMax 
                elif event.code == 'ABS_RY':
                    self.RJY = event.state / XboxController.joyMax
                elif event.code == 'ABS_RX':
                    self.RJX = event.state / XboxController.joyMax 
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state

    def hapticFeedback(self,vibType,length,gamepad=None):
        if not gamepad:
            gamepad = inputs.devices.gamepads[0]
        if vibType == 0:                              #Low freq high amp (left motor)
            gamepad.set_vibration(1, 0,length)
        elif vibType == 1:                            #High freq low amp (right motor)
            gamepad.set_vibration(0, 1, length)


def get_angle(dy,dx):  #Works out the angle based on the opposite and adjacent sides dependant on the quadrant
    ang = 0
    if dx>0 and dy>0: #q1
        ang = math.degrees(math.atan(abs(dx)/abs(dy)))
    elif dx>0 and dy<0: #q2
        ang = math.degrees(math.atan(abs(dy)/abs(dx)))+90
    elif dx<0 and dy<0: #q3
        ang = math.degrees(math.atan(abs(dx)/abs(dy)))+180
    elif dx<0 and dy>0: #q4
        ang = math.degrees(math.atan(abs(dy)/abs(dx)))+270
    elif dx==0 and dy==0:        #Checks for special case where angle is on quadrant boundries
        ang = 0
    elif dx == 0 and dy > 0:
        ang = 0
    elif dx == 0 and dy < 0:
        ang = 180
    elif dx > 0 and dy == 0:
        ang = 90
    elif dx > 0 and dy == 0:
        ang = 270

    return round(ang,1)

def min_angle_difference(a1,a2):       #Works out the minimum difference in angle between two angles
    if a2-a1 < 0:
        sign = -1
    else:
        sign = 1
    da = abs(a2-a1)
    if da > 180:
        da = 360 - da
    return da*sign

def get_room(odom,rooms):
    for room in rooms:          #Check what room robot is in
        if odom[0][0] > room[1][0] and odom[0][0] < room[2][0]:
            if odom[0][1] > room[1][1] and odom[0][1] < room[2][1]:
                return room[0]


if  __name__ == "__main__":
    c = XboxController()                       #Creates Controller class
    print('Starting Engine')                   
    eng = matlab.engine.start_matlab()         #Starts the matlab engine
    print('Engine started')
    ip = str(input("Enter the IP address of the robot: "))
    eng.connectRob(ip,nargout=0)                  #Connects to ROS network and sets up environment variables
    start = round(time.time(),2)               #Sets the start time of the program
    prevSec = 0
    moved = False
    forwardVel = 0.32                          #Define the max velocities
    spinVel = -0.72
    crash = 0
    mostConfident = [0,0,0,0,0]

    rooms = [                                  #List of rooms and thier boundaries
        ['Main',[-6.2,-2.2],[2.3,2]],
        ['LittleRoom',[2.3,-2.2],[7,2]],
        ['BigRoom',[-6.2,2],[7,5.6]],
        ]
    POIs = {                                    #Dictionary of POIs in each room
        "Main": [(2.3,0.6,0),(-3,-1.5,0),(-6.0,0,90),(-4.5,2,270)],
        "LittleRoom": [(2.3,0.6,180),(4.5,-1.7,0),(6,0,270),(4.5,2,270)],
        "BigRoom": [(4.5,2,90),(-4.5,2,90),(6.25,4,180),(-2,4.5,180)],
    }


    while True:
        sec = round(time.time(),2)-start
        if round(sec,2) == prevSec:           #Tic every 0.5 seconds
            if not moved:
                odom = eng.getOdom()            #Make sure not already moved this tic
                test = eng.avoidObstacles()     #Get odometry and make sure that robot is not close to an obstacle
                while test == 1:                #If too close to an obstacle, obtain the steering direction
                    if c.LJX == 0:
                        steeringDir = 0
                    elif c.LJY == 0:
                        steeringDir = c.LJX
                    else:
                        steeringDir = math.atan(c.LJY+0.001/c.LJX+0.001)
                        
                    if steeringDir > 0:
                        steeringDir = steeringDir-1.5708
                    else:
                        steeringDir = steeringDir+1.5708
                    c.hapticFeedback(1,5)                   #Vibrate the controller
                    eng.autopilot(steeringDir,nargout=0)    #Give control to the autopilot until the obstacle is cleared
                    test = eng.avoidObstacles()             #Check if obstacle cleared


                v = round(c.LJY,1)           #Get controller inputs
                a = round(c.LJX,1)
                
                if odom[0][3] < 0:              #Convert odometry angle to bearing
                    odomAng = odom[0][3]+360
                else:
                    odomAng = odom[0][3]

                room = get_room(odom,rooms)     #Check the current room

                mostConfident = [0,0]
                for point in POIs[room]:        #Check which point in the room has the highest confidence score
                    x1 = odom[0][0]
                    y1 = odom[0][1]
                    x2 = point[0]
                    y2 = point[1]
                    theta = point[2]

                    relAng = odom[0][3]*-1     #Work oout he angle between the x axis and the robot as bearing
                    if relAng < 0:
                        relAng = relAng+360

                    relAng = round(relAng)+90  #Shift bearing to the x axis

                    if relAng >= 360:                #Correct overbearing
                        relAng = relAng-360


                    dy = round((y2-y1),1)           #Find the x and y distances between robot and POI
                    dx = round((x2-x1),1)


                    ang = get_angle(dy,dx)          

                    stickAng = get_angle(round(c.LJY,1),round(c.LJX,1))     #Get the stick angle

                    adjustedStickAng = stickAng+relAng                      #Adjust the stick angle to correct coordinate frame
                    if adjustedStickAng >= 360:
                        adjustedStickAng = adjustedStickAng-360


                    da = min_angle_difference(adjustedStickAng,ang)     #Find the minumnum angle difference between the stick and point

                    ConfidenceScore = math.exp((-1/180)*abs(da))*0.8       #Calculate the confidence score

                    if ConfidenceScore > mostConfident[1]:                      #Check if its the largest so far
                        mostConfident = [da,ConfidenceScore,x2,y2,theta]

                da = mostConfident[0]                                       #Angle difference of the most confident point

                ConfidenceScore = (mostConfident[1]-0.5)*2                  #Adjust confidence score to make less aggressive

                if ConfidenceScore < 0:                                     #If less than zero disregard
                    ConfidenceScore = 0

                vel = (v*(1-ConfidenceScore)) + 1*ConfidenceScore           #Scale velocity to both inputs using confidence score

                eng.minimap(odom[0][0],odom[0][1],mostConfident[2],mostConfident[3],nargout=0)  #Display the minimap

                if abs(da) > 40:                                                #If angle is more than 40 (roughly the max rotation in one tic of the algorithm)
                    if da < 0:
                        avel = (a*(1-ConfidenceScore)) + -1*ConfidenceScore     #Rotate max in the correct direction
                    else:
                        avel = (a*(1-ConfidenceScore)) + 1*ConfidenceScore
                else:
                    avel = (a*(1-ConfidenceScore)) + (da/40)*ConfidenceScore    #If less than 40 rotate a scaled amount to avoid over rotation

                if c.A == 1:                                                    #Only move if the A button is pressed
                    eng.moveRob(vel*forwardVel,avel*spinVel,nargout=0)
                elif c.A != 1:
                    eng.moveRob(0.0,0.0,nargout=0)                              #Else completely stop
                if c.B == 1:
                    break                                                       #Exit loop
        else:
            moved = False
        prevSec = round(time.time()-start,1)                                    #Update the previous second to avoid looping too fast

    eng.moveRob(0.0,0.0,nargout=0)                                              #Bring the robot to a halt before disconnecting
    eng.disconnectRob(nargout=0)