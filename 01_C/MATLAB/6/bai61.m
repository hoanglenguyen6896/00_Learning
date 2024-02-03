clear all, close all;
imRGB = imread('img.png');
figure; 
imshow(imRGB); 
title('RGB Full Image');
imYIQ = rgb2ntsc(imRGB);

imYIQsubI = imresize(imYIQ(:,:,2),0.5,'bilinear');
imYIQsubQ = imresize(imYIQ(:,:,3),0.5,'bilinear');

imYIQupsampI = imresize(imYIQsubI,2);
imYIQupsampQ = imresize(imYIQsubQ,2);

reconstruct_imYIQ = imYIQ;
reconstruct_imYIQ(:,:,2) = imYIQupsampI;
reconstruct_imYIQ(:,:,3) = imYIQupsampQ;

reconstruct_imRGB = uint8(256*ntsc2rgb(reconstruct_imYIQ));
figure; 
imshow(reconstruct_imRGB);
title('Reconstruct RGB Full Image');

figure;
imshow(256*abs(imRGB(:,:,1)-reconstruct_imRGB(:,:,1))); 
title('Reconstruct R Error');
figure; 
imshow(256*abs(imRGB(:,:,2)-reconstruct_imRGB(:,:,2))); 
title('Reconstruct G Error');
figure; 
imshow(256*abs(imRGB(:,:,3)-reconstruct_imRGB(:,:,3))); 
title('Reconstruct B Error');