image_original = imread('pca.bmp');
% 原图显示
subplot(2, 3, 1);
imshow(image_original, []);
Entropy_original = entropy(image_original)
title_0 = strcat('Original Image  Information:', num2str(Entropy_original))
title(title_0);

% 获取源图像大小，进行奇异值分解，提供压缩
% 利用奇异值分解可以对任意形状的图片进行压缩处理，不仅限于 n*n 的图片
% 对于同一个方阵(n*n)矩阵，进行特征值分解和奇异值分解的结果是相同的
% A = Q^-1 * S * Q // A = u * S * v
[m ,n] = size(image_original);
[u, s, v] = svd(double(image_original));

% when Compress rate - 2:1
% 根据压缩比例取得对应的K值(K值越大，则压缩的比例越小，损失程度的较小)
rate_1 = 2;
K = round(2 * m * n / ((m + n + 1) * rate_1))
if K > min(m, n)
    K = min(m, n);
end
image_compress_1 = zeros(size(image_original));
% 根据压缩的比例不同，压缩之后的数据只需传输svd分解之后向量/矩阵的前K个数值(u,S,v)即可，这就是压缩之后的结果
% 获取前K特征值(前K个大奇异值，以及对应的左/右奇异值向量)进行图像解压缩还原
for i = 1 : K
    image_compress_1 = image_compress_1 + (s(i , i) * u(: , i) * v(: , i)');
end
subplot(2, 3, 4);
imshow(image_compress_1, []);
imwrite(uint8(image_compress_1), '1.bmp');
% 经过特定比例压缩之后的图像的信息量计算
Entropy_1 = entropy(imread('1.bmp'));
title_1 = strcat('Compress Rate 2:1  Information:', num2str(Entropy_1))
title(title_1);

% 之后重复上面的操作，只是改变了压缩比例
% when Compress rate - 8:1
rate_2 = 8;
K = round(2 * m * n / ((m + n + 1) * rate_2))
if K > min(m, n)
    K = min(m, n);
end
image_compress_2 = zeros(size(image_original));
for i = 1 : K
    image_compress_2 = image_compress_2 + s(i, i) * u(: , i) * v(: , i)';
end
subplot(2, 3, 5);
imshow(image_compress_2, []);
imwrite(uint8(image_compress_2), '2.bmp');
Entropy_2 = entropy(imread('2.bmp'));
title_2 = strcat('Compress Rate 8:1  Information:', num2str(Entropy_2))
title(title_2);

% when Compress rate - 32:1
rate_3 = 32;
K = round(2 * m * n / ((m + n + 1) * rate_3))
if K > min(m, n)
    K = min(m, n);
end
image_compress_3 = zeros(size(image_original));
for i = 1 : K
    image_compress_3 = image_compress_3 + s(i, i) * u(: , i) * v(: , i)';
end
subplot(2, 3, 6);
imshow(image_compress_3, []);
imwrite(uint8(image_compress_3), '3.bmp');
Entropy_3 =  entropy(imread('3.bmp'));
title_3 = strcat('Compress Rate 32:1  Information:', num2str(Entropy_3))
title(title_3);