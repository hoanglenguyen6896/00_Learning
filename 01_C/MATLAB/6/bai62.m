clc, clear all, close all;
I = imread('img1.bmp');
I1 = I;
I2 = double(I);
[row, coln] = size(I);
I = double(I);
I = I-(128*ones(256));

QX =[16 11 10 16 24 40 51 61;
    12 12 14 19 26 58 60 55;
    14 13 16 24 40 57 69 56;
    14 17 22 29 51 87 80 62;
    18 22 37 56 68 109 103 77;
    24 35 55 64 81 104 113 92;
    49 64 78 87 103 121 120 101;
    72 92 95 98 112 100 103 99];

DCT_matrix8 = dct(eye(8));
iDCT_matrix8 = DCT_matrix8';

dct_restore = zeros(row,coln);
QX = double(QX);

for i1=[1:8:row]
    for i2=[1:8:coln]
        zBLOCK = I(i1:i1+7,i2:i2+7);
        win1 = DCT_matrix8*zBLOCK*iDCT_matrix8;
        dct_domain(i1:i1+7,i2:i2+7) = win1;
    end
end

for i1=[1:8:row]
    for i2=[1:8:coln]        
        win1 = dct_domain(i1:i1+7,i2:i2+7);
        win2 = round(win1./QX);
        dct_quantized(i1:i1+7,i2:i2+7) = win2;
    end
end

for i1=[1:8:row]
    for i2=[1:8:coln]        
        win2 = dct_quantized(i1:i1+7,i2:i2+7);
        win3 = win2.*QX;
        dct_dequantized(i1:i1+7,i2:i2+7) = win3;
    end
end

for i1=[1:8:row]
    for i2=[1:8:coln]        
        win3 = dct_dequantized(i1:i1+7,i2:i2+7);
        win4 = iDCT_matrix8*win3*DCT_matrix8;
        dct_restore(i1:i1+7,i2:i2+7) = win4;
    end
end
I2 = dct_restore;
K=mat2gray(I2);
figure;
imshow(I1); 
title('Original Img');
figure;
imshow(K); 
title('Restore Img from dct');

mse = mean(mean(I2-K).^2);
peaksnr = 10*log10(255^2/mse);