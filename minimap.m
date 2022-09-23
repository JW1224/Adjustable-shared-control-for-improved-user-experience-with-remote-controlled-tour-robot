function minimap(sx,sy,gx,gy)
    figure(1)           %Access the correct figure
    hold on             %Hold plots on figure
    map = evalin("base","Map");     %Retieve map
    show(map)               %Show map on figure
    plot([sx gx], [sy gy],"k--d")       %plot line between locationa and goal
    plot(sx,sy,'ro','MarkerSize',20)    %Add markers for the points
    plot(gx,gy,'bo','MarkerSize',20)
    hold off            %Remove hold so plot can be refreshed
end