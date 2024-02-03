function generalComp(OriginalImage,img_m,img_h,img_hm,img_a1,img_a10)
figure;
subplot(2,3,1);
imshow(OriginalImage);
title('Original Pic.');
subplot(2,3,2);
imshow(img_m);
title('SMQT (L=8)');
subplot(2,3,3);
imshow(img_h);
title('Histogram Equalization');
subplot(2,3,4);
imshow(img_hm);
title('Histogram Equalization (Matlab)');
subplot(2,3,5);
imshow(img_a1);
title('HSV, V transform algorithm (n=1)');
subplot(2,3,6);
imshow(img_a10);
title('HSV, V transform algorithm (n=10)');

figure;
if(size(OriginalImage,3)<=1)
    subplot(2,3,1);
    imhist(OriginalImage);
    title('Original histogram');
    subplot(2,3,2);
    imhist(img_m);
    title('SMQT histogram (L=8)');
    subplot(2,3,3);
    imhist(img_h);
    title('Histogram Equalization');
    subplot(2,3,4);
    imhist(img_hm);
    title('Histogram Equalization (Matlab)');
    subplot(2,3,5);
    imhist(img_a1);
    title('HSV, V transform algorithm (n=1)');
    subplot(2,3,6);
    imhist(img_a10);
    title('HSV, V transform algorithm (n=10)');
else
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(OriginalImage);
    subplot(2,3,1);
    plot(xr,yRed,'r',xg,yGreen,'g',xb,yBlue,'b');
    title('Original histogram');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_m);
    subplot(2,3,2);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('SMQT histogram (L=8)');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_h);
    subplot(2,3,3);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('Histogram Equalization');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_hm);
    subplot(2,3,4);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('Histogram Equalization (Matlab)');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_a1);
    subplot(2,3,5);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('HSV histogram, V transform algorithm (n=1)');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_a10);
    subplot(2,3,6);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('HSV histogram, V transform algorithm (n=10)');
end
end