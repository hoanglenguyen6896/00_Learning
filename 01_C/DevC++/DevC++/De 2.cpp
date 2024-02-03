#include "stdio.h"
#include "conio.h"
main()
{
	int i, a[8], t, n, j, k;
	printf("Nhap cac phan tu cua mang:\n");
    for(i=0;i<7;i++)
	{
		printf("Phan tu thu %d\n", i+1);
		scanf("%d", &t);
		if(t != 0)
		{
			a[i]=t;
			n=i+1;
		}
	    else
	    {
	    	n=i;
	    	break;
	    }
	}
	printf("\nMang vua nhap la:\n");
	for(i=0;i<n;i++)
	{
		printf("%-4d", a[i]);
	}
	for(i=0;i<n-1;i++)
	{
		for(j=i+1;j<n;j++)
		{
			if(a[i]<a[j])
			{
				k=a[i];
				a[i]=a[j];
				a[j]=k;
			}
		}
	}
	printf("\nMang sau khi sap xep la:\n");
	for(i=0;i<n;i++)
	{
		printf("%-4d", a[i]);
	}
	   
	getch();
}
