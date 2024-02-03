function [ outspeech ] = speechcoder1(inspeech)
if(nargin ~=1)
    error('argument check failed');
end;
Fs = 16000;
Order = 10;
[aCoeff, resis, pitch, G, parcor, stram] = proclpc(inspeech, Fs, Order);
outspeech = synlpc(aCoeff, pitch, Fs, G)