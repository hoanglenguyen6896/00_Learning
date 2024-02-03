#include "MKL46Z4.h"
//#include <stdio.h>

char a = 125;
int kcs;

void checker()
{
    int a = 0;
    a++;
    a++;
    kcs = 10;
}

int add(int a, int b/*, int c, int d, int e, int f, int g, int h, int a1, int a2,
        int a3, int a4, int a5, int a6, int a7, int a8*/)
{
    int k;
    k = a + b /*+ c + d + e + f +g+h+a1+a2+a3+a4+a5+a6+a7+a8*/;
    //checker();
    return k;
}

int address(int *a1, int *a2/*, int *a3, int *a4, int *a5, int *a6, int *a7, int *a8,
            int *a9, int *a10, int *a11, int *a12, int *a13, int *a14, int *a15, int *a16*/)
{
    int x;
    x= *a1 + *a2 /*+ *a3 + *a4 + *a5 + *a6 + *a7 + *a8 + *a9 + *a10 + *a11 + *a12 + *a13 + *a14
        + *a15 + *a16*/;
    return x;
}
int main(void)
{
    int c = 0;
    int ccccca = 0;

    int a1 = 10;
    int a2 = 10 + a1;
    int a3 = 10 + a2;
    int a4 = 10 + a3;
    int a5 = 10 + a4;
    int a6 = 10 + a5;
    int a7 = 10 + a6;
    int a8 = 10 + a7;
    int a9 = 10 + a8;
    int a10 = 10 + a9;
    int a11 = 10 + a10;
    int a12 = 10 + a11;
    int a13 = 10 + a12;
    int a14 = 10 + a13;
    int a15 = 10 + a14;
    int a16 = 10 + a15;
    //printf("%d", 123);
    checker();

    c = add(a1,a2/*,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15, a16*/);
    ccccca = address(&a1,&a2/*,&a3,&a4,&a5,&a6,&a7,&a8,&a9,&a10,&a11,&a12,&a13,&a14,&a15,&a16*/);
    while(0);




}