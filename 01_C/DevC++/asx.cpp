#include "stdio.h"
#include "conio.h"
main()
{
	int a=0,b=0,c=0,d=0;
	int max1 = 0, max2 = 0, max3 = 0;
	for(a=0; a<10; a++)
	{
		for(b=10; b>a ; b--)
		{
			printf(" ");
		}
		for(c=0; c<a ; c++)
		{
			printf("%d", c+1);
		}
		for(d=a-1; d>0 ; d--)
		{
			printf("%d", d);
		}
		printf("\n");
	}
	getch();
}
