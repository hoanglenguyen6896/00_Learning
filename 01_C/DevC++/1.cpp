#include "stdio.h"
#include "conio.h"
#include "math.h"
main()
{
	static float a, b;
	static float c;
	static int d;
	printf("Nhap 2 so a b lan luot la: \n");
	scanf("%d", &a);
	scanf("%d", &b);
	c = a/b;
	d =round(c);
	printf("%f %d", c, d);
	return 0;
}
