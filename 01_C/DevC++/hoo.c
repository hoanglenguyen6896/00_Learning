#include <stdio.h>
#include <stdlib.h>

#define MAX_INX	5

struct tester {
	int a;
	int b;
	int c;
	int *d;
};



main()
{
	struct tester test[MAX_INX];
	int i = 0;
	int j = 0;
	int ks = 2;
	for(i=0; i<MAX_INX; i++)
	{
		test[i].a = i + ks*i;
		test[i].b = i + ks*ks*i;
		test[i].c = i + ks*ks*i*i;
		test[i].d = (int*) calloc(i+1, sizeof(int));
		
		printf("%d\n", *test[i].d);
		printf("--%d\n", *test[i].d);
		for(j=0; j<5; j++)
		{
			printf("jj--%x\n", (test[i].d + j));
		}
		ks++;
	}
	for(i=0; i<MAX_INX; i++)
	{
		free(test[i].d);
	}
//	printf("%p", test[5].d);
//	free(test[0].d);
//	free(test[1].d);
//	free(test[2].d);
	return 0;
}
