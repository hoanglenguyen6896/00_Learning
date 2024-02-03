#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "parseSREC.h"

/*
SType	ByteCount	Address		Data	Checksum
*/
int main()
{
	char cSrecLine[1000];
	uint8_t iEndFile = 0u;
	int i = 0u;
	long int positionChecking = 0u;
	uint8_t iIs32bits = 0u; /*S37-style 32-bit address records S0357*/
	uint8_t iIs24bits = 0u; /*S28-style 24-bit address records S0258*/
	uint8_t iIs16bits = 0u; /*S19-style 16-bit address records S0159*/
	uint8_t iFileError = 0u;
	
	record rLineContent;
	
    FILE *fptr;
    fptr = fopen("srecTemp", "r");
    if(fptr == NULL)
    {
    	printf("Error!");
	}
	/* Get 1 line per loop */
	while(iEndFile == 0u)
	{
		vReadLineS(cSrecLine, 516u, fptr);
		if(feof(fptr)) iEndFile = 1u;
		else
		{
			puts(cSrecLine);
			vGetSS(cSrecLine, &rLineContent);
			//puts(rLineContent.cSTypes);
			printf("%s ",rLineContent.cSTypes);
			
			vGetByteCountS(cSrecLine, &rLineContent);
			//puts(rLineContent.cByteCount);
			printf("%s ",rLineContent.cByteCount);
			
			vGetAddressS(cSrecLine, &rLineContent);
			//puts(rLineContent.cAdress);
			printf("%s ",rLineContent.cAdress);
			
			vGetDataS(cSrecLine, &rLineContent);
			printf("%s ",rLineContent.cData);
			
			vGetChecksumS(cSrecLine, &rLineContent);
			//puts(rLineContent.cChecksum);
			printf("%s ",rLineContent.cChecksum);
			printf("\n-------------------------------------------------------\n");
		}
	}
	fclose(fptr);
	return 0u;
}




