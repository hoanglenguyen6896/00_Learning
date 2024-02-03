#include <stdio.h>
int check(int number)
{
	int count = 0;
	int index = 0;
	
	if(number < 2)
	{
		return 0;
	}
	for (index = 2; index <= number - 1; index++)
	{
		if(number % index == 0)
		{
			count++;
		}
	}
	
	if(count == 0)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

int main()
{
	int n = 0;
	int result = 0;
	printf("Nhap so n =");
	scanf("$d",&n);
	result = check(n);
	if(result == 0)
	{
		printf("%d khong phai la so nguyen to", n);
	}
	else
	{
		printf("%d la so nguyen to", n);
	}
}

