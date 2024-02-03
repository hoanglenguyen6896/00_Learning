#include <stdio.h>

struct tester {
	int a;
	int b;
	int c;
	int *d;
};

main()
{
	struct tester test[3];
	printf("%x", test[4].d);
	return 0;
}
