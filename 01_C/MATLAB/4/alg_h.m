function Output = alg_h(Input)
[row,column,d] = size(Input);
i = 0;
while(i<d)
    i = i+1;
    histo = imhist(Input(:,:,i));
    Input(:,:,i) = double (Input(:,:,i));
    probability = histo./(row*column);
    equalizer = cumsum(probability)*256;
    Output(:,:,i) = equalizer(Input(:,:,i)+1);
Input = uint8(Input);
Output = uint8(Output);
end