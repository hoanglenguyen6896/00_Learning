#include "stdio.h"
#include "conio.h"
#include "math.h"
main()
{
	int n=0;
	float m=1, Pis=0;
	float epsilon;
	do
	{
		printf("Nhap so epsilon (0 < epsilon < 1): "); scanf("%f", &epsilon);
	}while(epsilon <= 0 || epsilon >= 1);
	while (fabs(m) >= epsilon)
	{
		m=pow(-1,n)/(2*n+1);
		Pis=Pis + m;
		n++;
	}
	printf("pi=%f", 4*Pis);
	getch();
}
