#ifndef      __A_H__
#define      __A_H__

#include "SRECprocess.h"
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

/*******************************************************************************
 * Function name: iCharToHex
 * Function: Convert 2 character to Hex
 ******************************************************************************/
uint8_t iCharToHex(char* cByte)
{
	uint8_t iFirst = 0;
	uint8_t iSecond = 0;

	if(cByte[0] >= '0' && cByte[0] <= '9') iFirst = cByte[0] - '0';
	else iFirst = cByte[0] - 'A' + 10;
	if(cByte[1] >= '0' && cByte[1] <= '9') iSecond = cByte[1] - '0';
	else iSecond = cByte[1] - 'A' + 10;
	return (iFirst*16 + iSecond);
}

/*******************************************************************************
 * Function name: vPrintError
 * Function: Print error: checksum, Byte count, Character, S type, Hex
 ******************************************************************************/
void vPrintError(uint8_t iChkFlag, uint16_t iLine, uint8_t *iEnd)
{
	if(iChkFlag == 30u)
	{
		printf("Loi Checksum o dong thu %d\n", iLine+1);
		*iEnd = 1u;
	}
	else if(iChkFlag == 20u)
	{
		printf("Loi Byte Count o dong thu %d\n", iLine+1);
		*iEnd = 1u;
	}
	else if(iChkFlag == 11u)
	{
		printf("Loi so luong ky tu o dong thu %d\n", iLine+1);
		*iEnd = 1u;
	}
	else if(iChkFlag == 12u)
	{
		printf("Loi S type o dong thu %d\n", iLine+1);
		*iEnd = 1u;
	}
	else if(iChkFlag == 33u)
	{
		printf("Loi ky tu khong la ma hex o dong thu %d\n", iLine+1);
		*iEnd = 1u;
	}
	else if(iChkFlag == 50u)
	{
		printf("Loi khong co Header S0 o dong thu 1\n");
		*iEnd = 1u;
	}
	else if(iChkFlag == 51u)
	{
		printf("Loi co nhieu du lieu o dong thu 2\n");
		*iEnd = 1u;
	}
	else if(iChkFlag == 52u)
	{
		printf("Loi thu tu du lieu o dong thu %d\n", iLine+1);
		*iEnd = 1u;
	}
}

/*******************************************************************************
 * Function name: vReadLineS
 * Function: Get 1 line of SREC file
 ******************************************************************************/
void vReadLineS(char* cLine, uint16_t iLength, FILE *ptr)
{
	uint16_t positionChecking = 0u;
	uint16_t i = 0u;
	fgets(cLine, iLength, ptr);
	cLine[strlen(cLine) - 1u] = '\0';
}

/*******************************************************************************
 * Function name: vGetStype
 * Function: Get Record Type of a SREC file's line
 ******************************************************************************/
void vGetStype(char* cLine, char * cStype)
{
	strncpy(cStype, cLine, 2u);
	cStype[2u] = '\0';
}

/*******************************************************************************
 * Function name: vGetByteCountS
 * Function: Get Byte Count of a SREC file's line
 ******************************************************************************/
void vGetByteCountS(char* cLine, char *cByteCount)
{
	strncpy(cByteCount, cLine + 2u, 2u);
	cByteCount[2u] = '\0';
}

/*******************************************************************************
 * Function name:vGetAddressS
 * Funtion:Get Address field of a SREC file's line
 ******************************************************************************/
void vGetAddressS(char* cLine, char *cAddress)
{
	char cStype[3] = {'\0','\0','\0'};
	vGetStype(cLine, cStype);
	/* 16 bits address */
	if(strcmp(cStype,"S0") == 0u || strcmp(cStype,"S1") == 0u
	||	strcmp(cStype,"S5") == 0u || strcmp(cStype,"S9") == 0u)
	{
		strncpy(cAddress, cLine + 4u, 4u);
		cAddress[4] = '\0';
	}
	/* 24 bits address */
	if(strcmp(cStype,"S2") == 0u ||	strcmp(cStype,"S6") == 0u
	|| strcmp(cStype,"S8") == 0u)
	{
		strncpy(cAddress, cLine + 4u, 6u);
		cAddress[6] = '\0';
	}
	/* 32 bits address */
	if(strcmp(cStype,"S3") == 0u || strcmp(cStype,"S7") == 0u)
	{
		strncpy(cAddress, cLine + 4u, 8u);
		cAddress[8] = '\0';
	}
}

/*******************************************************************************
 * Function name: vGetChecksumS
 * Function: Get Checksum of a SREC file's line
 ******************************************************************************/
void vGetChecksumS(char* cLine, char *cCheckS)
{
	strncpy(cCheckS, cLine + strlen(cLine) - 2u, 2u);
	cCheckS[2u] = '\0';
}

/*******************************************************************************
 * Function name: vGetDataS
 * Function: Get Data field of a SREC file's line
 ******************************************************************************/
void vGetDataS(char* cLine, char *cData)
{
	uint16_t iDataSize = 0u;
	uint16_t i = 0u;
	char cSType[3] = {'\0','\0','\0'};
	char cCheckS[3] = {'\0','\0','\0'};
	char cByteCount[3] = {'\0','\0','\0'};
	char cAddress[9] = {'\0','\0','\0','\0','\0','\0','\0','\0','\0'};
	vGetStype(cLine,cSType);
	vGetChecksumS(cLine, cCheckS);
	vGetByteCountS(cLine, cByteCount);
	vGetAddressS(cLine, cAddress);
	iDataSize = strlen(cLine) - strlen(cSType)	- strlen(cCheckS)
								- strlen(cByteCount) - strlen(cAddress);
	for(i=0; i<100; i++)
	{
		cData[i] = '\0';
	}
	if(iDataSize == 0) ;
	else
	{
		strncpy(cData, cLine + 2u + 2u + strlen(cAddress), iDataSize);
	}
}

void vCheckS56789size(char* cLine, char *iEnd)
{
	if(cLine[1] == '5' || cLine[1] == '9')
	{
		if(strlen(cLine) != 10) *iEnd = 1;
	}
	else if(cLine[1] == '6' || cLine[1] == '8')
	{
		if(strlen(cLine) != 12) *iEnd = 1;
	}
	else if(cLine[1] == '7')
	{
		if(strlen(cLine) != 14) *iEnd = 1;
	}
}

/*******************************************************************************
 * Function name: iCheckChar
 * Function: Checking if a line character error or not
 * Return 11 if the number of characters is error
 * Return 13 if a character is not a hexa (except char[0] and char[1])
 * Return 12 char[0] and char[1] is not a sequence of S1 - S9 (except S4)
 * Return 16 if no error
 ******************************************************************************/
uint8_t iCheckChar(char* cLine)
{
	uint8_t iKeyChk = 0u;
	uint8_t iChk = 0u;
	uint8_t i = 0u;

	if((strlen(cLine)%2u) != 0u) iKeyChk = 11u;
	else
	{
		if(cLine[0] == 'S')
		{
			if(cLine[1] >= '0' && cLine[1] <= '9' && cLine[1] != '4')
			{
				for(i=2u; i<strlen(cLine)-1; i++)
				{
					if(cLine[i] >= '0' && cLine[i] <= '9') iKeyChk = 16u;
					else if(cLine[i] >= 'A' && cLine[i] <= 'Z') iKeyChk = 16u;
					else iKeyChk = 13u;
				}
			}
			else iKeyChk = 12u;
		}
		else iKeyChk = 12u;
	}
	return iKeyChk;
}

/*******************************************************************************
 * Function name: iCheckChar
 * Function: Checking if byte count error or not
 * Return 21 if no error byte count
 * Return 20 if Byte Count error
 ******************************************************************************/
uint8_t iCheckByteCount(char* cLine)
{
	char cByteCount[3] = {'\0','\0','\0'};
	uint8_t iByteCount = 0u;
	uint8_t iBcChk = 0u;
	uint8_t iS56789 = 0u;
	vGetByteCountS(cLine, cByteCount);
	iByteCount = iCharToHex(cByteCount);
	if(iByteCount < 3) iBcChk = 20u;
	if((strlen(cLine) - 4u)/2u == iByteCount)
	{
		vCheckS56789size(cLine, &iS56789);
		if(iS56789 == 1) iBcChk = 20u;
		else iBcChk = 21u;
	}
	else iBcChk = 20u;
	return iBcChk;
}

/*******************************************************************************
 * Function name: iAddressSum
 * Function: Return Sum of Address in a SREC line
 ******************************************************************************/
uint16_t iAddressSum(char* cLine)
{
	uint16_t iAddS = 0u;
	uint8_t i = 0u;
	char cAdd[9];
	char cAddTemp[3] = {'\0','\0','\0'};
	vGetAddressS(cLine, cAdd);
	for(i=0u; i<strlen(cAdd)/2; i++)
	{
		strncpy(cAddTemp, cAdd +i*2u, 2u);
		iAddS += iCharToHex(cAddTemp);
	}
	return iAddS;
}

/*******************************************************************************
 * Function name: iDataSum
 * Function: Return Sum of Data in a SREC line
 ******************************************************************************/
uint16_t iDataSum(char* cLine)
{
	uint16_t iDataS = 0u;
	uint8_t i = 0u;
	char cData[100];
	char cDataTemp[3] = {'\0','\0','\0'};
	vGetDataS(cLine, cData);
	for(i=0u; i<strlen(cData)/2; i++)
	{
		strncpy(cDataTemp, cData +i*2u, 2u);
		iDataS += iCharToHex(cDataTemp);
	}
	return iDataS;
}

/*******************************************************************************
 * Function name: iCheckSum
 * Function: Checking if Checksum error or not
 * Return 31 if no error byte count
 * Return 30 if Byte Count error
 ******************************************************************************/
uint8_t iChecksum(char* cLine)
{
	char cChecksum[3] = {'\0','\0','\0'};
	char cByteCount[3] = {'\0','\0','\0'};
	uint8_t iChecksum = 0u;
	uint8_t iSum = 0u;
	uint8_t iCsChk = 0u;
	vGetChecksumS(cLine, cChecksum);
	vGetByteCountS(cLine, cByteCount);
	iSum = iCharToHex(cChecksum) + iDataSum(cLine)
			+ iCharToHex(cByteCount) + iAddressSum(cLine);
	iSum = iSum & 0xFF;
	if(iSum == 0xFF) iCsChk = 31;
	else iCsChk = 30;
	return iCsChk;
}

/*******************************************************************************
 * Function name: iCheckSRECLine
 * Function: Checking char 1, bytecount 2, checksum 3
 * Return 31 if 1 2 3 true
 * Return 30 if Checksum error
 * Return 20 if Bytecount error
 * Return 11 if Number of character in a Line is error
 * Return 12 if S type is error
 * Return 13 if a character is not a hexa number
 ******************************************************************************/
uint8_t iCheckSRECLine(char* cLine)
{
	uint8_t iLastChk = 0u;
	uint8_t iByteCountChk = 0u;
	uint8_t iChkSum = 0u;
	/* Check char (all) */
	iLastChk = iCheckChar(cLine);

	if(iLastChk == 16u)
	{
		/* Check bytecount (all) */
		iByteCountChk = iCheckByteCount(cLine);
		if(iByteCountChk == 21u)
		{
			/* Checksum (all) */
			iChkSum = iChecksum(cLine);
			iLastChk = iChkSum;
		}
		else iLastChk = 20u;
	}
	return iLastChk;
}

/*******************************************************************************
 * Function name: vCheck1stLine
 * Function: Checking Header line is S0 and is valid or not
 ******************************************************************************/
void vCheck1stLine(char* cLine, uint16_t iLine, uint8_t* iEnd, uint8_t *iFile)
{
	if(cLine[0] == 'S' && cLine[1] == '0')
	{
		vPrintError(iCheckSRECLine(cLine), iLine, iEnd);
	}
	else
	{
		vPrintError(50u, 0u, iEnd);
	}
	if(*iEnd == 1) *iFile = 1;
	else *iFile = 0;
}

/*******************************************************************************
 * Function name: vCheck2ndLine
 * Function: Checking if 2nd line
 ******************************************************************************/
void vCheck2ndLine(char* cLine, uint16_t iLine,
						uint8_t* iEnd, uint8_t *iFile, uint8_t *iAdd)
{
	if(cLine[1] == '0' || cLine[1] == '5' || cLine[1] == '6'
			|| cLine[1] == '7' || cLine[1] == '8' ||cLine[1] == '9')
	{
		vPrintError(51u, 1u, iEnd);
	}
	else
	{
		*iAdd = (cLine[1] - '0')*8+8;
		vPrintError(iCheckSRECLine(cLine), 1u, iEnd);
	}
	if(*iEnd == 1) *iFile = 1;
	else *iFile = 0;
}

void iCountS5S6byAddress(char* Add, uint8_t* AddDec, uint32_t *count)
{
	uint8_t i = 0;
	uint32_t iCountTotal = 0;
	for(i=0u; i<strlen(Add); i++)
	{
		if(*(Add+i) >= '0' && *(Add+i)<= '9')
			*(AddDec+i) = *(Add+i) - '0';
		else *(AddDec+i) = *(Add+i)- 'A' + 10;
	}
	for(i=0u; i<strlen(Add); i++)
	{
		*count+=*(AddDec+i)*pow(16u,strlen(Add)-1-i);
	}
}
#endif

