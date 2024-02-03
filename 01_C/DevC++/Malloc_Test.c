#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
int main(void)
{
    uint8_t* checker = NULL;
	uint8_t* checker2 = NULL;
    uint8_t* checker3 = NULL;
    uint8_t* checker4 = NULL;
    static uint8_t i = 0;
    checker = calloc(1,sizeof(uint8_t));
    checker2 = calloc(2,sizeof(uint8_t));
    checker3 = calloc(8,sizeof(uint8_t));
    checker4 = calloc(17,sizeof(uint8_t));
    
//    checker = realloc(checker,10);
//    checker2 = realloc(checker2,10);
//    checker3 = realloc(checker3,10);
//    checker4 = realloc(checker4,10);
    for(i=0; i<50; i++)
    {
     	printf("a[%d] = %d\t", i, *(checker+i));
    }
    printf("\n\n");
    for(i=0; i<50; i++)
    {
    	printf("b[%d] = %d\t", i, *(checker2+i));
    }
    printf("\n\n");
    for(i=0; i<50; i++)
    {
     	printf("c[%d] = %d\t", i, checker3[i]);
    }
    printf("\n\n");
    for(i=0; i<50; i++)
    {
     	printf("d[%d] = %d\t", i, checker4[i]);
    }
    free(checker);
    free(checker2);
    free(checker3);
    free(checker4);
    return 0;

}
