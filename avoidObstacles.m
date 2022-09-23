function crash = avoidObstacles()
    crash = 0;
    laser = evalin("base","scan"); %Retrieve subscriber
    scan = receive(laser,3);        %Recieve scan

    data = rosReadCartesian(scan);    %Read the scan
    x = data(:,1);
    y = data(:,2);

    dist = sqrt(x.^2 + y.^2);       %Pythoagoras for each distance to find shortest
    minDist = min(dist);
    if minDist < 0.5                %If less than the min distance return crash as 1
        crash = 1;
    end
end
