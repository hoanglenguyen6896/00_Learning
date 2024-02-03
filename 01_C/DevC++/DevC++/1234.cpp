#include "stdio.h"
#include "conio.h"
int gt(int x)
{
	int i,y=1;
	for(i=1; i<=x; i++) y=y*i;
	return y;
}
int A(int k, int n)
{
	int y;
	y=gt(n)/gt(n-k);
	return y;
}
int F(int k, int n)
{
	int y;
	if (k<0 || n<0 || k>n) y=0;
	else y=2*A(k,n) + 3*A(n-k,n);
	return y;
}
main()
{
	int i, n, a[16], max;;
	while(n<2 || n>10)
	{
		printf("Nhap so nguyen n (2<=n<=10): "); scanf("%d", &n);
	}
	for(i=0; i<=n; i++)
	{
		a[i]=F(i,n);
	}
	max=a[0];
	for(i=0; i<=n; i++)
	{
		if (a[i]>max) max=a[i];
	}
	printf("%d", max);
	getch();
}
