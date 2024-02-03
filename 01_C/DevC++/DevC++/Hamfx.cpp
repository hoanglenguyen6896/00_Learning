#include "stdio.h"
#include "conio.h"
float hamfx(float x)
{
	float y;
	y=2*x*x*x*x-3;
	return y;
}
main()
{
	int i;
	float t, k=0;
	printf("Nhap so thuc bat ki: "); scanf("%f", &t);
	for(i=0; i<=19; i++)
	{
		t=t-0.02*i;
		printf("f(%.2f)=%f\n", t, hamfx(t));
	}
	getch();
}
