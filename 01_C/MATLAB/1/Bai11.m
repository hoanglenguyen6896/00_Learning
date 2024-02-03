A = imread('img.jpg');
figure;
imshow(A);

figure;
B=A; C=A; D=A;
B(:,:,2)=0; B(:,:,3)=0;
C(:,:,1)=0; C(:,:,3)=0;
D(:,:,1)=0; D(:,:,2)=0;

subplot(231); imshow(B); title('R');
subplot(232); imshow(C); title('G');
subplot(233); imshow(D); title('B');

subplot(234); imhist(A(:,:,1)); title('Histogram R');
subplot(235); imhist(A(:,:,2)); title('Histogram G');
subplot(236); imhist(A(:,:,3)); title('Histogram B');

figure;
A1=rgb2gray(A);
subplot(1,3,1); imshow(A1); title('Anh xam');
subplot(1,3,2); imhist(A1); title('Histogram anh xam');
A1_adj=imadjust(A1,[0.3,0.7],[]);
subplot(1,3,3); imshow(A1_adj); title('Anh tang tuong phan');

figure;
amban=255.-A1;
subplot(121); imshow(amban); title('Anh am ban');
subplot(122); imhist(amban); title('Histogram anh am ban');

