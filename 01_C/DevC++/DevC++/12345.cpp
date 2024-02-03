#include "stdio.h"
#include "conio.h"
#include "math.h"
main()
{
	int a=5, b=4;
	a^=b^=a^=b;
	printf("%d %d", a, b);
	getch();
}
