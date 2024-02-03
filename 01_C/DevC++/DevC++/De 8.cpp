#include "stdio.h"
#include "conio.h"
main()
{
	int i, a[16], b[16], N;
	int max=0, min=0, max2=0;
	printf("Nhap so nguyen N (0<N<10): N="); scanf("%d", &N);
	while(N<=0 || N>=10)
	{
		printf("Nhap lai N (0<N<10): N="); scanf("%d", &N);
	}
	printf("Nhap mang %d so nguyen:\n", N);
	for(i=0;i<=N-1;i++)
	{
		printf("a[%d]=", i);
		scanf("%d", &a[i]);
	}
	max=a[0];
	printf("Mang vua nhap la: ");
	for(i=0;i<=N-1;i++)
	{
		printf("%-5d", a[i]);
		if(a[i]>=max) max=a[i];
	}
	if(N==1) printf("\nDay chi gom 1 phan tu, khong co phan tu thu 2");
	else
	{
	for(i=0;i<=N-1;i++) b[i]=max-a[i];
	min=max;
	for(i=0;i<=N-1;i++)
	{
		if(b[i]==0) continue;
		else 
		{
			if (b[i]<min)
			{
				 min=b[i];
				 max2=a[i];
			}
		}
		
	}
	if (min==max) printf("\nKhong co so lon thu 2");
	else printf("\nSo lon thu 2 trong day la %d", max2);
	}
	getch();
}
