function odom = getOdom()
    sub = evalin("base","odomsub");   %Retrieve subscriber
    odomMsg = receive(sub,10);         %Recieve the odometry
    
    pose = odomMsg.Pose.Pose;           %Access the ppose
    x = pose.Position.X;
    y = pose.Position.Y;
    z = pose.Position.Z;

    quat = pose.Orientation;            %Calculate orientation
    angles = quat2eul([quat.W quat.X quat.Y quat.Z]);
    theta = rad2deg(angles(1));    %Convert to degrees

    odom = [x,y,z,theta];           %Return odometry data as list
end