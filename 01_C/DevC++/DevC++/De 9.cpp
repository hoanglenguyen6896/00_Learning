#include "stdio.h"
#include "conio.h"
main()
{
	int N, a[16], i, x=0, T=0;
	float Tb=0;
	printf("Nhap so nguyen N (0<N<10): N="); scanf("%d", &N);
	while(N<=0 || N>=10)
	{
		printf("Nhap la N (0<N<10): N="); scanf("%d", &N);
	}
	printf("Nhap mang N so nguyen :\n");
	for(i=0;i<=N-1;i++)
	{
		printf("a[%d]=", i); scanf("%d", &a[i]);
	}
	printf("Mang vua nhap la:");
	for(i=0;i<=N-1;i++) printf("%5d", a[i]);
	for(i=0;i<=N-1;i++)
	{
		if(a[i]%5 == 0 && a[i]%10 != 0)
		{
			T=T+a[i];
			x++;
		}
	}
	if(x==0) printf("\nKhong co so chia het cho 5 nhung khong chia het cho 10 trong day");
	else
	{
		Tb=T/x;
	    printf("\nTrung binh cong cac so chia het cho 5 nhung khong chia het cho 10 trong day la %.2f", Tb);	
    }
	getch();
}
