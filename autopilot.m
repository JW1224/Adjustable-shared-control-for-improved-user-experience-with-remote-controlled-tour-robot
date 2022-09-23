function autopilot(dir)
    targetDir = double(dir);  %Convert the target direction to a matlab accepted data type
    laserScan = evalin("base","scan");  %Retrieve the scan subscriber
    scan = receive(laserScan);          %Recieve the scan
    ranges = double(scan.Ranges);       %Seperate the angle and ranges from scan struct
    angles = rosReadScanAngles(scan);

    vfh = evalin("base","vfh");         %Retrieve the VFH object

    scanData = lidarScan(ranges,angles);    %Create lidar scan from ranges and angles

    steeringDirection = vfh(scanData,targetDir);    %pass variable to object

    if ~isnan(steeringDirection) % Check if steering direction is valid
		v = 0.32;           %max forward velocity

        curPose = [0 0 0];  %current pose in reference frame (oriented around robot so 0s)
        wMax = 0.72;        %max rotational speed
		
        lookaheadPoint = [cos(steeringDirection), sin(steeringDirection)]; %find the lookahead point
        slope = atan2((lookaheadPoint(2) - curPose(2)),(lookaheadPoint(1) - curPose(1)));   %Find the slope to he lookagead point
        a = angdiff(curPose(3), slope);     %Find angle change need to rotate to the lookahead point

        w = (2*sin(a));                     %Find roational speed needed to achieve this

        if abs(abs(a) - pi) < 1e-12
            w = sign(w)*1;
        end

        if abs(w) > wMax
            w = sign(w)*wMax;
        end

    else
		v = 0.0;        %If not safe direction found rotate on the spot
		w = 0.72;
    end

    moveRob(v,w)          %Move the robot based on calculated velocities
end