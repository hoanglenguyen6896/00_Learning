#include "stdio.h"
#include "conio.h"
main()
{
	int N, X, i, a[16], j=0;
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
	printf("\nNhap so nguyen X (X<10): X="); scanf("%d", &X);
	while(X>=10)
	{
		printf("Nhap lai X (X<10): X="); scanf("%d", &X);
	}
	for(i=0; i<=N-1; i++)
	{
		if(a[i]==X) j++;
    }
    printf("So luong cac so trong day co gia tri bang %d la: %d", X, j);
    getch();
}
