#include "stdio.h"
#include "conio.h"
main()
{
	int N, i, j, T=0, a[16], sl=0, vt;
	printf("Nhap so nguyen N (0<N<10): N="); scanf("%d", &N);
	while(N<=0 || N>=10)
	{
		printf("Nhap lai so nguyen N (0<N<10): N="); scanf("%d", &N);
	}
	printf("Nhap mang %d so nguyen:\n", N);
	for(i=0 ; i<=N-1; i++)
	{
		printf("a[%d]=", i); scanf("%d", &a[i]);
	}
	printf("\nMang vua nhap la:");
	for(i=0; i<=N-1; i++)
	    printf("%5d", a[i]);
	for(i=0; i<=N-1; i++)
	{
		T=0;
		for(j=1; j<=a[i]; j++)
		{
			if (a[i]%j == 0)
			{
				T=T+j;
			}
		}
		if (T==2*a[i])
		{
			sl++;
			vt=i+1;
			printf("\nVi tri so hoan thien thu %d la: %d", sl, vt);
		}
	}
	printf("\nSo luong so hoan thien trong day la %d", sl);
	getch();
}
