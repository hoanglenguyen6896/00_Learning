#include "stdio.h"
#include "conio.h"
main()
{
	int M, N, i, TM=0, TN=0;
	printf("Nhap so nguyen M="); scanf("%d", &M);
	while(M<=1 || M>=2000)
	{
		printf("Nhap lai M (1<M<2000): M="); scanf("%d", &M);
	}
	printf("Nhap so nguyen N="); scanf("%d", &N);
	while(N<=1 || N>=2000)
	{
		printf("Nhap lai N (1<N<2000): N="); scanf("%d", &N);
	}
	for(i=1; i<=M/2; i++)
	{
		if (M%i==0) TM += i;
	}
	for(i=1; i<=N/2; i++)
	{
		if (N%i==0) TN += i;
	}
	if (M==TN-1 && N==TM-1) printf("Day la cap so hua hon");
	else printf("Day khong phai cap so hua hon");
	getch();
}
