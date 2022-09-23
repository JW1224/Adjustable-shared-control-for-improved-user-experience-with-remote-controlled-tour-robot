function moveRob(v,a)
    robotCmd = evalin('base','robotCmd');  %Retrieve publisher and message from workspace
    velMsg = evalin('base', 'velMsg');
    
    velMsg.Linear.X = double(v);            %Alter message to given velocites
    velMsg.Angular.Z = double(a);
    send(robotCmd,velMsg)                   %send message
end