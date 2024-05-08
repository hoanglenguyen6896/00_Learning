%M? Video .avi
obj = VideoReader('gra.mp4');
implay('gra.mp4');
nFrames = obj.NumberofFrames;
Rate = obj.FrameRate;
%Hi?n th? 10 khung ??u ti�n
for k = 1:10
    this_frame = read(obj, k);
    thisfig = figure();
    image(this_frame);
    title(sprintf('Frame #%d', k));
end
%T?o ho�n v? ng?u nhi�n t? 1 ??n nFrames
MatrixA = randperm(nFrames);

%T?p video b?ng ho�n v? ?� t?o ? tr�n
newavi = VideoWriter('newvideo.avi');
newavi.FrameRate = obj.FrameRate;
open(newavi);

for g=1:1:nFrames
    index = MatrixA(g)
    this_frame = read(obj, index);
    writeVideo(newavi,this_frame);
end
disp('Closing movie file');
close(newavi);
disp('display newvideo');
implay('newvideo.avi');