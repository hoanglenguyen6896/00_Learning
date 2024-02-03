Amax = zeros(16);
Amax(6:11,6:11) = 255;
subplot(121); imshow(Amax); title('Anh ban dau');
A1=Amax(1:8,1:8); A2=Amax(1:8,9:16); 
A3=Amax(9:16,1:8); A4=Amax(9:16,9:16);
A1_dct=dct2(A1); A2_dct=dct2(A2); 
A3_dct=dct2(A3); A4_dct=dct2(A4);
Q=[16 11 10 16 24 40 51 61;
   12 12 14 19 26 58 60 55;
   14 13 16 24 40 57 69 56;
   14 17 22 29 51 87 80 62;
   18 22 37 56 68 109 103 77;
   24 35 55 64 81 104 113 92;
   49 64 78 87 103 121 120 101;
   72 92 95 98 112 100 103 99];

A1_lt=A1_dct./Q; A2_lt=A2_dct./Q; 
A3_lt=A3_dct./Q; A4_lt=A4_dct./Q;

A1_I=idct2(A1_lt); A2_I=idct2(A2_lt); 
A3_I=idct2(A3_lt); A4_I=idct2(A4_lt);

Ares(1:8,1:8)=A1_I; Ares(1:8,9:16)=A2_I; 
Ares(9:16,1:8)=A3_I; Ares(9:16,9:16)=A4_I;
subplot(122); imshow(Ares); title('Anh sau khi nen');
