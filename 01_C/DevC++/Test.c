#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>

#define CUR_WORKING_DIR "PWD"   /* Current working directory */
#define PERMISSION_MASK 0777u   /* Permission mask */
#define DIR_NAME_SIZE   256u

uint8_t* strCat(uint8_t *strDestination, uint8_t *strSource)
{
    uint8_t strIndex;
    uint8_t strDesLen = strlen(strDestination);
    // printf("--x--\n");
    for(strIndex = 0u; strIndex < strlen(strSource); strIndex++)
    {
        // printf("%d ",strlen(strDestination));
        strDestination[strDesLen + strIndex] = strSource[strIndex];
    }
    // printf("\n%s\n", strDestination);
    return strDestination;
}

void inputArray(int a[][100], int n)
{
	int i = 0;
	int j = 0;
	
	for(i=0; i<n; i++)
	{
		for(j=0; j<n; j++)
		{
			printf("Nhap a[%d][%d] = ",i , j);
			scanf("%d", &a[i][j]);
		}
	}
}

float findMax(float a[], int n)
{
	int i = 0;
	float max = a[0];
	for(i=1; i<n; i++)
	{
		if(a[i] > max)
		{
			max = a[i];
		}
	}
	return max;
}

int main(void)
{
//    uint8_t a[100] = "HoangLe";
//    uint8_t b[100] = "Nguyen";
//    printf("\n*****abcdef*****\n");
//    printf("%s", strCat(a,b));
//	int p = 4;
//	p = 10 + ++p;
//	printf("%d", p);
//    return 0u;

//	int i = 0;
//	int j = 0;
//	int arr[100][100];
	int n = 1;
//	float a[3] = {1.2, 0.12, 4.5};
	float a[1] = {1.2};
	float x = findMax(a, 1);
	printf("%f", x);
	return 0;
}

