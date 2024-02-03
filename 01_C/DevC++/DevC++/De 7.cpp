#include "stdio.h"
#include "conio.h"
main()
{
	int a[16], T=0, x=0, i, N;
	float Tb=0;
	printf("Nhap so nguyen N (0<N<10): N="); scanf("%d", &N);
	while(N<=0 || N>=10)
	{
		printf("Nhap lai N (0<N<10): N="); scanf("%d", &N);
	}
	printf("Nhap mang %d so nguyen:\n", N);
	for(i=0;i<=N-1;i++)
	{
		printf("a[%d]=", i); scanf("%d", &a[i]);
		if (a[i]%2==1)
		{
			T=T+a[i];
			x++;
		}
	}
	printf("Mang vua nhap la:");
	for(i=0;i<=N-1;i++)
		printf("%-5d", a[i]);
	if (x==0) printf("\nTrung binh cong cua cac so le co trong day la: 0");
	else 
	{
		Tb=T/x;
		printf("\nTrung binh cong cua cac so le trong day la %.2f", Tb);
	}
	getch();
}
