function [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(image)
Red = image(:,:,1);
Green = image(:,:,2);
Blue = image(:,:,3);
[yRed,xr] = imhist(Red);
[yGreen,xg] = imhist(Green);
[yBlue,xb] = imhist(Blue);
end