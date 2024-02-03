#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include "SRECprocess.h"

/*
SType	ByteCount	Address		Data	Checksum
*/
int main()
{
	char cSRECLine[100];
	char cData[100];
	char cAdd[16];
	char cS56Stype[3];
	char cS56DataAddress[8];
	uint8_t cS56DataAddressDec[8];

	uint32_t iS1S2S3Count = 0u;
	uint32_t iS1S2S3CountByS56 = 0u;
	uint8_t iUseS5OrS6;
	uint32_t iLineCount = 0u;

	uint8_t iAddType = 0u;
	uint8_t iEndFile = 0u;
	uint8_t iEndDataLine = 0u;
	uint8_t i = 0u;

	uint8_t iFileError = 0u;

    FILE *fSREC;
    FILE *fOutput;
    fSREC = fopen("srec2", "r");
    if(fSREC == NULL)
    {
    	uint8_t iFileError = 1u;
    	printf("Error! when openning file\n");
    	iEndFile = 1;
    	iFileError = 1;
	}

	/* Get 1 line per loop */
	while(iEndFile == 0u)
	{
		vReadLineS(cSRECLine, 516u, fSREC);
		if(feof(fSREC))
		{
			iEndFile = 1u;
			iLineCount--;
		}
		else
		{
			/* Checking if 1st line error or not (S0) */
			if(iLineCount == 0u)
			{
				vCheck1stLine(cSRECLine, iLineCount, &iEndFile, &iFileError);
			}
			/* Checking Data type in 2nd line (S1/S2/S3) */
			else if(iLineCount == 1u)
			{
				vCheck2ndLine(cSRECLine, iLineCount,
							&iEndFile, &iFileError, &iAddType);
			}
			/* Checking if the remain line error or not */
			else if(iLineCount > 1u)
			{

				/*
				* Checking Data type, if file contain only 1 type
				* (S1/S2/S3) or not
				* If true, check if it's from 5 - 9 or not
				*/
				if(iAddType != (cSRECLine[1] - '0')*8u+8u)
				{
					if((cSRECLine[1] == '5' || cSRECLine[1] == '6')
								&& iEndDataLine == 0)
					{
						vPrintError(iCheckSRECLine(cSRECLine),
								iLineCount,&iEndFile);
						if(iEndFile == 0)
						{
							iEndDataLine = 1;
							vGetAddressS(cSRECLine, cS56DataAddress);
							vGetStype(cSRECLine, cS56Stype);
						}
						else
						{
							iFileError = 1;
						}
					}
					else if((cSRECLine[1] == '7' || cSRECLine[1] == '8'
								|| cSRECLine[1] == '9')
								&& iEndDataLine == 1)
					{
						vPrintError(iCheckSRECLine(cSRECLine),
								iLineCount,&iEndFile);
						if(iEndFile == 0)
						{
							iEndDataLine = 2;
						}
						else iFileError = 1;
					}
					else
					{
						vPrintError(52u, iLineCount, &iEndFile);
						iFileError = 1;
					}
				}
				else if(iEndDataLine == 1 || iEndDataLine == 2)
				{
					vPrintError(52u, iLineCount-1, &iEndFile);
					iFileError = 1;
				}
				/*
				* If Data type is the same with 2nd line,
				* just do normal checking
				*/
				else
				{
					vPrintError(iCheckSRECLine(cSRECLine),iLineCount,&iEndFile);
					if(iEndFile==1) iFileError = 1;
				}
			}
		}
		iLineCount++;
	}
	/* Count number of Data line */
	iS1S2S3Count = iLineCount - 3;
	if(iS1S2S3Count < 65536u) iUseS5OrS6 = 5;
	else iUseS5OrS6 = 6;
	iCountS5S6byAddress(cS56DataAddress,cS56DataAddressDec,&iS1S2S3CountByS56);
	
	if(iS1S2S3Count != iS1S2S3CountByS56 && iFileError == 0)
	{
		iFileError = 1;
		printf("Loi tong so Data Line S1/S2/S3 va Count Line S5/S6 ");
		printf("o dong thu %d\n", iLineCount-1);
	}
	/* Checking S5/s6 */
	if(iFileError == 0)
	{
		if(iUseS5OrS6 == 5 && cS56Stype[1] == '6')
		{
			printf("Loi so luong S1/S2/S3 < 65536 nhung su dung S6 ");
			printf("o dong %d\n", iLineCount-1);
			iFileError = 1;
		}
		else if (iUseS5OrS6 == 6 && cS56Stype[1] == '5')
		{
			printf("Loi so luong S1/S2/S3 >= 65536 nhung su dung S5 ");
			printf("o dong %d\n", iLineCount-1);
			iFileError = 1;
		}
	}
	iEndFile = 0;
	/*  */
	
	fOutput = fopen("output.txt", "w");
	if(fOutput == NULL)
    {
    	uint8_t iFileError = 1u;
    	printf("Error! when openning file\n");
    	iEndFile = 1;
    	iFileError = 1;
	}
	if(iFileError == 0)
	{
		fseek(fSREC,0,SEEK_SET);
		printf("Khong co loi\n");
		while(iEndFile == 0u)
		{
			vReadLineS(cSRECLine, 516u, fSREC);
			if(feof(fSREC))
			{
				iEndFile = 1u;
			}
			else
			{
				vGetDataS(cSRECLine, cData);
				vGetAddressS(cSRECLine, cAdd);
				
				fputs(cAdd,fOutput);
				fputs(" ",fOutput);
				fputs(cData,fOutput);
				fputs("\n",fOutput);
				fflush(fOutput);
			}
		}
	}
	fclose(fOutput);
	fclose(fSREC);
	if(iFileError == 0) system("output.txt");
	return 0u;
}

