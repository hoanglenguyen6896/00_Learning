% Record your voice for 5 seconds.
recObj = audiorecorder;
disp('Start speaking.')
recordblocking(recObj, 5);
disp('End of Recording.');

% Play back the recording.
play(recObj);


% Store data in double-precision array.
myRecording = getaudiodata(recObj);

filename = 'hoangLe.wav';
audiowrite(filename,myRecording,10000);
clear myRecording Fs
% Plot the waveform.

[myRecording,Fs] = audioread(filename);
plot(myRecording);