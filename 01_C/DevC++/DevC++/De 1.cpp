#include "stdio.h"
#include "conio.h"
int main()
{
	int N, X, T=0, i, a[16],t;
	float M=0,Tb=0;
	printf("Nhap so nguyen N (0<N<10): N="); scanf("%d", &N);
	while(N>=10 || N<=0)
	{
		printf("N khong hop le, nhap lai N (0<N<10): "); 
		scanf("%d", &N);
	}
	printf("Nhap mang %d so\n", N);
	for(i=0;i<N;i++)
	{
		printf("a[%d]=", i);
		scanf("%d", &a[i]);
	}
	printf("Mang vua nhap la:\n");
	for(i=0;i<N;i++)
	{
		printf("%-5d", a[i]);
	}
	printf("\nNhap so nguyen X bat ki: X="); scanf("%d", &X);
	if(X<=N)
	{
		for(i=0;i<X;i++)
		{
			M=M+a[i];
		}
		Tb=M/X;
		printf("Trung binh cong cua %d so dau trong mang la %.1f", X, Tb);
	}
	else
	{
		for(i=0;i<N;i++)
		{
			T=T+a[i];
		}
		printf("Tong cac so trong mang la %d", N, T);
	}
	getch();
}
