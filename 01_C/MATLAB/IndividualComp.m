function IndividualComp(OriginalImage,img_m,img_h,img_hm,img_a1,img_a10);
%Anh goc SQMT
figure;
subplot(2,2,1);
imshow(OriginalImage);
title('Original Pic.');
subplot(2,2,3);
imshow(img_m);
title('SMQT (L=8)');
if(size(OriginalImage,3)<=1)
    subplot(2,2,2);
    imhist(OriginalImage);
    title('Originl histogram');
    subplot(2,2,4);
    imhist(img_m)
    title('SMQT histogram (L=8)');
else
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(OriginalImage);
    subplot(2,2,2);
    plot(xr,yRed,'r',xg,yGreen,'g',xb,yBlue,'b');
    title('Original histogram');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_m);
    subplot(2,2,4);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('SMQT histogram (L=8)');
end
%Can bang bieu do
figure;
subplot(2,2,1);
imshow(OriginalImage);
title('Original Pic.');
subplot(2,2,3);
imshow(img_h);
title('Histogram Equalization');
if(size(OriginalImage,3)<=1)
    subplot(2,2,2);
    imhist(OriginalImage);
    title('Original histogram');
    subplot(2,2,4);
    imhist(img_h);
    title('Histogram Equalization');
else
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(OriginalImage);
    subplot(2,2,2);
    plot(xr,yRed,'r',xg,yGreen,'g',xb,yBlue,'b');
    title('Original histogram');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_h);
    subplot(2,2,4);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('Histogram Equalization');
end
%Matlab
figure;
subplot(2,2,1);
imshow(OriginalImage);
title('Original histogram');
subplot(2,2,3);
imshow(img_hm);
title('Histogram Equalization (Matlab)');
if(size(OriginalImage,3)<=1)
    subplot(2,2,2);
    imhist(OriginalImage);
    title('Original histogram');
    subplot(2,2,4);
    imhist(img_hm);
    title('Histogram Equalization');
else
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(OriginalImage);
    subplot(2,2,2);
    plot(xr,yRed,'r',xg,yGreen,'g',xb,yBlue,'b');
    title('Original histogram');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_hm);
    subplot(2,2,4);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('Histogram Equalization (Matlab)');
end
%HSV (n=1)
figure;
subplot(2,2,1);
imshow(OriginalImage);
title('Original histogram');
subplot(2,2,3);
imshow(img_a1);
title('HSV, V transform algorithm (n=1)');
if(size(OriginalImage,3)<=1)
    subplot(2,2,2);
    imhist(OriginalImage);
    title('Original histogram');
    subplot(2,2,4);
    imhist(img_a1);
    title('HSV histogram, V transform algorithm (n=1)');
else
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(OriginalImage);
    subplot(2,2,2);
    plot(xr,yRed,'r',xg,yGreen,'g',xb,yBlue,'b');
    title('Original histogram');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_a1);
    subplot(2,2,4);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('HSV histogram, V transform algorithm (n=1)');
end
%HSV (n=10)
figure;
subplot(2,2,1);
imshow(OriginalImage);
title('Original histogram');
subplot(2,2,3);
imshow(img_a10);
title('HSV, V transform algorithm (n=10)');
if(size(OriginalImage,3)<=1)
    subplot(2,2,2);
    imhist(OriginalImage);
    title('Original histogram');
    subplot(2,2,4);
    imhist(img_a10);
    title('HSV histogram, V transform algorithm (n=10)');
else
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(OriginalImage);
    subplot(2,2,2);
    plot(xr,yRed,'r',xg,yGreen,'g',xb,yBlue,'b');
    title('Original histogram');
    [yRed,xr,yGreen,xg,yBlue,xb] = splitRGB(img_a10);
    subplot(2,2,4);
    plot(xr,yRed,'Red',xg,yGreen,'Green',xb,yBlue,'Blue');
    title('HSV histogram, V transform algorithm (n=10)');
end
end