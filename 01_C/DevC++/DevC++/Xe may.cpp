#include "stdio.h"
#include "conio.h"
#include "string.h"
typedef struct xemay
{
	char hang[21];
	int namsx;
} xe;
main()
{
	int i, x=0;
	xe a[30];
	for(i=0; i<=1; i++)
	{
		printf("Nhap thong tin xe thu %d\n", i+1);
		printf("     Hang san xuat: ");
		fflush(stdin); gets(a[i].hang);
		printf("     Nam san xuat: "); scanf("%d", &a[i].namsx);
	}
	for (i=0; i<=1; i++)
	{
		printf("Thong tin xe thu %d\n", i+1); printf("     "Hang san xuat:" ");
		puts(a[i].hang); printf("     San xuat nam %d\n", a[i].namsx);
	}
	for(i=0; i<=1; i++)
	{
		if (strcmp("Honda", a[i].hang)==0)
		{
			x++;
			printf("Xe Honda thu %d san xuat nam %d\n", x, a[i].namsx);
		}
	}
	printf("Tong so xe Honda la: %d", x);
	getch();
}
