function[indx qy]= lquan(x,xmin,xmax,nbit)
nlevel= 2^nbit;
q= (xmax-xmin)/nlevel;
[indx qy] =quantiz(x,xmin+q:q:xmax-q,xmin+q/2:q:xmax-q/2);
