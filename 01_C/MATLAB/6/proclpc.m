function [aCoeff,resid,pitch,G,parcor,stream] = proclpc(data,sr,L,fr,fs,preemp)
if(nargin<3), L=10; end
if(nargin<4), fr = 20; end
if(nargin<5), fs=30; end
if(nargin<6), preemp=.9378; end
[row col] = size(data);
if col==1 data=data'; end
nframe = 0;
msfr = round(sr/1000*fr);
msfs = round(sr/1000*fs);
duration = length(data);
speech = filter([1-preemp],1,data)';
msoverlap = msfs-msfr;
ramp = [0:1/(msoverlap-1):1]';

for frameIndex = 1:msfr:duration-msfs+1
    frameData = speech(frameIndex:(frameIndex+msfs-1));
    nframe = nframe+1;
    autoCor = xcorr(frameData);
    autoCorVec = autoCor(msfs+[0:L]);
    err(1) = autoCorVec(1);
    k(1) = 0;
    A=[];
    for index=1:L
        numerator = [1 A']*autoCorVec(index+1:-1:2);
        denominator = -1*err(index);
        k(index) = numerator/denominator;
        A = [A+k(index)*flipud(A);k(index)];
        err(index+1) = (1-k(index)^2)*err(index);
    end
    aCoeff(:,nframe) = [1; A];
    parcor(:,nframe) = k';
    if 0
        gain =0;
        cft=0:(1/255):1;
        for index=1:L
            gain = gain + aCoeff(index,nframe)*exp(-i*2*pi*cft).^index;
        end
        gain=abs(1./gain);
        spec(:,nframe) = 20*log10(gain(1:128))';
        plot(20*log10(gain));
        title(nframe);
        drawnow;
    end
    if 0 
        impulseResponse = filter(1,aCoeff(:,nframe),[1 zeros(1,255)]);
        freqResponse = 20*log10(abbs(fft(impulseResponse)));
        plot(freqResponse);
    end
    errSig = filter([1 A'],1,frameData);
    G(nframe) = sqrt(err(L+1));
    autoCorErr = xcorr(errSig);
    [B,I] = sort(autoCorErr);
    num = length(I);
    if B(num-1)>.01*B(num)
        pitch(nframe) = abs(I(num) - I(num-1));
    else
        pitch(nframe) = 0;
    end
    resid(:,nframe) = errSig/G(nframe);
    if(frameIndex==1)
        stream =resid(1:msfr,nframe);
    else
        stream = [stream];
        overlap+resid(1:msoverlap,nframe).*ramp;
        resid(msoverlap+1:msfr,nframe);
    end
    if(frameIndex+msfr+msfs-1>duration)
        stream = [stream; resid(msfr+1:msfs,nframe)];
    else
        overlap = resid(msfr+1:msfs,nframe).*flipud(ramp);
    end
end
stream = filter(1,[1-preemp],stream)';