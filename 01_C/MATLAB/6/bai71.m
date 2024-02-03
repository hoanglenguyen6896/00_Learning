clc, clear all;
InputFilename = 'sound123.wav';
[inspeech, Fs, bits] = wavread(InputFilename);
outspeech1 = speechcoder1(inspeech);
figure; subplot(2,1,1); plot(inspeech);
grid;
subplot(2,1,2); plot(outspeech1); 
grid;