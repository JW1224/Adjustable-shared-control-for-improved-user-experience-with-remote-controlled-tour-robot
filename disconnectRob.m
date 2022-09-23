function disconnectRob()
    clear             %Clears the workspace
    rosshutdown         %Shutsdown matlab node and disconnects
    disp('Disconnected Successfuly')
end