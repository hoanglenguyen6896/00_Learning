function A = alg_m(RGBimage,l,n)
[row, column, d] = size(RGBimage);
if(d==3)
    HSVimage = rgb2hsv(RGBimage);
    V = HSVimage(:,:,3);
else
    V = double(RGBimage)/255;
end
V = V(:);
[Vsorted,ix] = sort(V);
s = (row*column)/n;
i = 0;
h = [];
while(i < n)
    i = i+1;
    z = Vsorted(((floor(s*(i-1))+1)):floor(s*i));
    Vstart = (s*(i-1))/(row*column);
    Vstop = (s*i)/(row*column);
    r = z - z(1)
    f = (1/n)/(r(size(r,1)));
    g = r*f;
    if(isnan(g(1)))
        g = r+Vstop;
    else
        g = g+Vstart;
    end
    h = vertcat(h,g);
end
m(ix) = h;
m = m(:);
if(d==3)
    HSVimage(:,:,3) = reshape(m,row,column);
    A = hsv2rgb(HSVimage);
else
    A = reshape(m,row,column);
end
return;
end