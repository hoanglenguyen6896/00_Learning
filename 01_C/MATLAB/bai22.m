t=0:0.01:20;
xt=sin(randn()+t).*cos(randn()*t);
[inx xqt] = lquan(xt,-1,1,randint(1,1,3)+2);
plot(t,xt,'b',t,xqt,'r');
grid on;