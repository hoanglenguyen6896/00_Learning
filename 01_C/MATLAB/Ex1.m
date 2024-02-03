[y,Fs] = audioread('NguyenLeHoang.m4a');
% Plot the waveform.
sound(y,Fs);
subplot(2,1,1);
plot(y);
title('time domain');

x=fft(y);
subplot(2,1,2);
plot(real(x));
title('freq domain');