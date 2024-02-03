#include "stdio.h"
#include "conio.h"
#include "math.h"
main()
{
	int N, i, a[16], j, t=0, s=0;
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
	printf("Mang vua nhap la: ");
	for(i=0;i<=N-1;i++)
	    printf("%-5d", a[i]);
	for(i=0;i<=N-1;i++)
	{
		if(a[i]<=1) t=1;
		else
		{
			for(j=2;j<=(int) sqrt(a[i]);j++)
			{
				if (a[i]%j==0) 
				{
					t=1;
					break;
				}
			}
			
	    }
	    if (t==0) s++;
	    else t=0;

	}
	printf("\nSo luong so nguyen to co trong day la %d", s);
	getch();
}
