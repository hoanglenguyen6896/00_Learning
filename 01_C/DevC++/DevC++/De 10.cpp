#include "stdio.h"
#include "conio.h"
main()
{
	int N, a[16], i, T, j, x=0;
	printf("Nhap so nguyen N (0<N<10): N="); scanf("%d", &N);
	while(N<=0 || N>=10)
	{
		printf("Nhap la N (0<N<10): N="); scanf("%d", &N);
	}
	printf("Nhap mang N so nguyen :\n");
	for(i=0;i<=N-1;i++)
	{
		printf("a[%d]=", i); scanf("%d", &a[i]);
	}
	printf("Mang vua nhap la:");
	for(i=0;i<=N-1;i++) printf("%5d", a[i]);
	for(i=0;i<=N-1;i++)
	{
		T=0;
		for(j=1; j<=a[i];j++)
		{
			if(a[i]%j == 0)
				T=T+j;
		}
		if(T==2*a[i]) x++;
	}
	printf("\nSo luong so hoan thien trong day la: %d", x);
	getch();
}
