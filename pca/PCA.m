image_original = imread('pca.bmp');
% ԭͼ��ʾ
subplot(2, 3, 1);
imshow(image_original, []);
Entropy_original = entropy(image_original)
title_0 = strcat('Original Image  Information:', num2str(Entropy_original))
title(title_0);

% ��ȡԴͼ���С����������ֵ�ֽ⣬�ṩѹ��
% ��������ֵ�ֽ���Զ�������״��ͼƬ����ѹ�������������� n*n ��ͼƬ
% ����ͬһ������(n*n)���󣬽�������ֵ�ֽ������ֵ�ֽ�Ľ������ͬ��
% A = Q^-1 * S * Q // A = u * S * v
[m ,n] = size(image_original);
[u, s, v] = svd(double(image_original));

% when Compress rate - 2:1
% ����ѹ������ȡ�ö�Ӧ��Kֵ(KֵԽ����ѹ���ı���ԽС����ʧ�̶ȵĽ�С)
rate_1 = 2;
K = round(2 * m * n / ((m + n + 1) * rate_1))
if K > min(m, n)
    K = min(m, n);
end
image_compress_1 = zeros(size(image_original));
% ����ѹ���ı�����ͬ��ѹ��֮�������ֻ�贫��svd�ֽ�֮������/�����ǰK����ֵ(u,S,v)���ɣ������ѹ��֮��Ľ��
% ��ȡǰK����ֵ(ǰK��������ֵ���Լ���Ӧ����/������ֵ����)����ͼ���ѹ����ԭ
for i = 1 : K
    image_compress_1 = image_compress_1 + (s(i , i) * u(: , i) * v(: , i)');
end
subplot(2, 3, 4);
imshow(image_compress_1, []);
imwrite(uint8(image_compress_1), '1.bmp');
% �����ض�����ѹ��֮���ͼ�����Ϣ������
Entropy_1 = entropy(imread('1.bmp'));
title_1 = strcat('Compress Rate 2:1  Information:', num2str(Entropy_1))
title(title_1);

% ֮���ظ�����Ĳ�����ֻ�Ǹı���ѹ������
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