function HistogramEqualization = alg_hm(OriginalImage)
[row,column,d] = size(OriginalImage);
i = 0;
while(i<d)
    i = i+1;
    HistogramEqualization(:,:,i) = histeq(OriginalImage(:,:,i));
end
end
