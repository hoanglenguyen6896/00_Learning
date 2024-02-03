function ImageEnhancement(OriginalImage)
OriginalImage = imread('fun.tif');
OriginalImage = uint8(OriginalImage);
img_m = alg_m(OriginalImage,1,8);
img_h = alg_h(OriginalImage);
img_hm = alg_hm(OriginalImage);
img_a1 = alg_a(OriginalImage,1);
img_a10 = alg_a(OriginalImage,10);
generalComp(OriginalImage,img_m,img_h,img_hm,img_a1,img_a10);
IndividualComp(OriginalImage,img_m,img_h,img_hm,img_a1,img_a10);
end