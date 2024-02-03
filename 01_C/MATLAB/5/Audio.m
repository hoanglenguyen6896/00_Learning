[data,sr] = audioread('Cantina.wav');
sound(data,sr);
subplot(2,1,1)
plot(data);
A=data.*30;
subplot(2,1,2);
plot(A);
pause(3.5);
sound(A,sr);