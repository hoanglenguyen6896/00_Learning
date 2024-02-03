#include "stdio.h"
#include "conio.h"
main()
{
	int N, i, x=0;
	float a[16], max;
	printf("Nhap so nguyen N (0<N<10): N="); scanf("%d", &N);
	while(N<=0 || N>=10)
	{
		printf("Nhap lai N (0<N<10): N=");
		scanf("%d", &N);
	}
	printf("Nhap mang %d so thuc:\n", N);
	for(i=0;i<=N-1;i++)
	{
		printf("a[%d]=", i);
		scanf("%f", &a[i]);
	}
	printf("Mang vua nhap la: ");
	for(i=0;i<=N-1;i++)
	{
		printf("%-8.2f", a[i]);
	}
	max=a[0];
	for(i=1;i<=N-1;i++)
	{
		if(a[i]>=max)
			max=a[i];
	}
	for(i=0;i<N;i++)
	{
		if(a[i]==max)
		    x++;
	}
	printf("\nGia tri lon nhat cua day la %f", max);
	printf("\nSo luong phan tu bang gia tri lon nhat la %d", x);
	getch();
}
