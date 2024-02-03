#include "stdio.h"
#include "conio.h"
#include "math.h"
main()
{
	int N, i, j, T=0, a[16], sl=0, sl1=0, vt;
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
	for(i=0; i<=N-1; i++)
	{
		T=0;
		if(a[i]<=1) continue;
	    else
	    {
	    	for(j=2; j<=(int) sqrt(a[i]); j++)
	    	{
	    		if(a[i]%j==0)
	    		{
	    			T++;
	    			break;
	    		}
	    	}
	    }
	    if(T==0)
	    {
	    	sl1++;
	    	if(a[i]<2015) sl++;
	    	vt=i+1;
	    	printf("\nVi tri SNT thu %d la %d", sl1, vt);
	    }
	}
	printf("\nSo luong SNT nho hon 2015 la: %d", sl);
	getch();
}
