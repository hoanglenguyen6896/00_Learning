#ifndef      __A_H__
#define      __A_H__

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

struct recordStructure
{
	char cSTypes[3u];
	char cByteCount[3u];
	char *cAdress;
	char *cData;
	char cChecksum[3u];
};
typedef struct recordStructure record;

/*******************************************************************************
 * Function Prototypes
 ******************************************************************************/

/* Read 1 line of file without position control position */
void vReadLineS(char* cLine, uint16_t iLength, FILE *ptr);
/* Get S type */
void vGetSS(char* cLine, record* rLineStructure);
/* Get Byte Count */
void vGetByteCountS(char* cLine, record *rLineStructure);

void vGetAddressS(char* cLine, record *rLineStructure);

void vGetAddress16bitsS(char* cLine, char **cAddress16);

void vGetAddress24bitsS(char* cLine, char **cAddress24);

void vGetAddress32bitsS(char* cLine, char **cAddress32);

void vGetChecksumS(char* cLine, record *rLineStructure);

void vGetDataS(char* cLine, record *rLineStructure);

/*******************************************************************************
 * Function Definition
 ******************************************************************************/

void vReadLineS(char* cLine, uint16_t iLength, FILE *ptr)
{
	uint16_t positionChecking = 0u;
	uint16_t i = 0u;
	fgets(cLine, iLength, ptr);
	cLine[strlen(cLine) - 1u] = '\0';
}

void vGetSS(char* cLine, record *rLineStructure)
{
	strncpy(rLineStructure->cSTypes, cLine, 2u);
	rLineStructure->cSTypes[2u] = '\0';
}

void vGetByteCountS(char* cLine, record *rLineStructure)
{
	strncpy(rLineStructure->cByteCount, cLine + 2u, 2u);
	rLineStructure->cByteCount[2u] = '\0';
}

void vGetAddressS(char* cLine, record *rLineStructure)
{
	/* 16 bits address */
	if(strcmp(rLineStructure->cSTypes,"S0") == 0u
	|| strcmp(rLineStructure->cSTypes,"S1") == 0u
	||	strcmp(rLineStructure->cSTypes,"S5") == 0u
	|| strcmp(rLineStructure->cSTypes,"S9") == 0u)
	{
		vGetAddress16bitsS(cLine, &rLineStructure->cAdress);
	}
	/* 24 bits address */
	if(strcmp(rLineStructure->cSTypes,"S2") == 0u
	||	strcmp(rLineStructure->cSTypes,"S6") == 0u
	|| strcmp(rLineStructure->cSTypes,"S8") == 0u)
	{
		vGetAddress24bitsS(cLine, &rLineStructure->cAdress);
	}
	/* 32 bits address */
	if(strcmp(rLineStructure->cSTypes,"S3") == 0u
	|| strcmp(rLineStructure->cSTypes,"S7") == 0u)
	{
		vGetAddress32bitsS(cLine, &rLineStructure->cAdress);
	}
}

void vGetAddress16bitsS(char* cLine, char **cAddress16)
{
	*cAddress16 = (char*) calloc(4u, 1u*sizeof(char));
	strncpy(*cAddress16, cLine + 4u, 4u);
}

void vGetAddress24bitsS(char* cLine, char **cAddress24)
{
	*cAddress24 = (char*) calloc(6u, 1u*sizeof(char));
	strncpy(*cAddress24, cLine + 4u, 6u);
}

void vGetAddress32bitsS(char* cLine, char **cAddress32)
{
	*cAddress32 = (char*) calloc(8u, 1u*sizeof(char));
	strncpy(*cAddress32, cLine + 4u, 8u);
}

void vGetChecksumS(char* cLine, record *rLineStructure)
{
	strncpy(rLineStructure->cChecksum, cLine + strlen(cLine) - 2u, 2u);
	rLineStructure->cChecksum[2u] = '\0';
}

void vGetDataS(char* cLine, record *rLineStructure)
{
	uint16_t iDataSize = 0u;
	iDataSize = strlen(cLine) - strlen(rLineStructure->cSTypes)
				- strlen(rLineStructure->cChecksum)
				- strlen(rLineStructure->cByteCount)
				- strlen(rLineStructure->cAdress);
	if(iDataSize == 0) rLineStructure->cData = NULL;
	else
	{
		rLineStructure->cData = (char*) calloc(iDataSize, 1u*sizeof(char));
		strncpy(rLineStructure->cData, cLine + 2u + 2u
										+ strlen(rLineStructure->cAdress),
										iDataSize);
	}
}

#endif

