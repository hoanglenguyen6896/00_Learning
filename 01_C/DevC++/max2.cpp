#include "stdio.h"
#include "conio.h"
main()
{
	char x = 'a';
	int a[4];
	int max1 = 0, i=0;
	for(i=0; i<=3 ; i++)
	{
		printf("Nhap so %c = ", x+i);
		scanf("%d", &a[i]);
		max1 = max1>a[i]?max1:a[i];
	}
	printf("So lon nhat trong 4 so la: %d", max1);
	getch();
}
