function connectRob(ipaddress)
    %% Connect to the ros network
    disp('Connecting to ros')
    rosinit(ipaddress)                                    %Connect to network
    %% Create Map
    topview = imread("MapOffice.png");                   %Read Map image
    invert = topview;                                    %Invert image colour
    BW = createMask(invert);                             %Create black and white image
    Map = binaryOccupancyMap(BW,10,"GridOriginInLocal",[-6 -2]);    %Create map from image and set coordinates
    mapInflated = copy(Map);                            %Inflate map
    inflate(mapInflated,0.15);
    assignin("base","Map",mapInflated)                  %Add to workspace
    assignin("base","defaultmap",Map)
    %% Set up avoidance
    vfh = controllerVFH;                                %Create controller object
    vfh.UseLidarScan = true;                            %Input parameters for object
    vfh.DistanceLimits = [0.05 2];
    vfh.RobotRadius = 0.15;
    vfh.MinTurningRadius = 0.01;
    vfh.SafetyDistance = 0.2;

    assignin("base","vfh",vfh)                          %Add to workspace
    %% Set up move publisher
    robotCmd = rospublisher("/cmd_vel","DataFormat","struct");  %Create publisher
    velMsg = rosmessage(robotCmd);                              %Create ros message
    assignin("base","robotCmd",robotCmd)                        %Add both to workspace
    assignin("base","velMsg",velMsg)
    %% Set up laserscan subscriber
    laser = rossubscriber("/scan","DataFormat","struct");       %Create subscriber
    assignin("base","scan",laser)                               %Add to workspace
    %% Set up camera subscriber
    camera = rossubscriber("/camera/rgb/image_raw/compressed",@displayImage,"DataFormat","struct");   %Create subscriber with callback function
    assignin("base","camera",camera)                                                                  %Add to workspace
    %% Set up odometry subsciber
    sub = rossubscriber("/odom","DataFormat","struct");           %Create subscriber
    assignin("base","odomsub",sub)                                %Add to workspace
    
%% Display Connnected
    disp('Connected Successfuly')
end