function displayImage(src,message)
    %src is not used but must be accepted as an argument as it will be
    %passed by the callback
    figure(2)    %Select correct figure
    img = rosReadImage(message);    %Read image from message passed
    imshow(img);        %Show the image on th figure
end