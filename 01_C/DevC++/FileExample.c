#include <stdio.h>
#include <stdlib.h>  /* For exit() function */
#include <string.h>

#define FOUR
#define FOUR(A,B)
#define FOUR (2 /* two */ + 2)

main()
{
	printf("CCCCCCCcccccc%dCCCCCCcccccc", FOUR);
//	char c[1000];
//	int i = 0;
//    FILE *fptr;
//    fptr = fopen("program.txt", "r");
//    if(fptr == NULL)
//   	{
//      printf("Error!");
//      exit(1);
//   	}
//	fscanf(fptr,"%[]", c);
//
//    for(i=0; i<strlen(c); i++)
//    {
//    	printf("%c", c[i]);
//	}
//	fclose(fptr);
//   	return 0;
}
