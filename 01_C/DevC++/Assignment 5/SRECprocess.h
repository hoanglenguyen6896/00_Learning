#ifndef      __A_H__
#define      __A_H__

uint8_t iCharToHex(char* cByte);

void vPrintError(uint8_t iChkFlag, uint16_t iLine, uint8_t *iEnd);

void vReadLineS(char* cLine, uint16_t iLength, FILE *ptr);

void vGetStype(char* cLine, char * cStype);

void vGetByteCountS(char* cLine, char *cByteCount);

void vGetAddressS(char* cLine, char *cAddress);

void vGetDataS(char* cLine, char *cData);

void vGetChecksumS(char* cLine, char *cCheckS);

void vCheckS56789size(char* cLine, char *iEnd);

uint8_t iCheckChar(char* cLine);

uint8_t iCheckByteCount(char* cLine);

uint16_t iAddressSum(char* cLine);

uint16_t iDataSum(char* cLine);

uint8_t iChecksum(char* cLine);

uint8_t iCheckSRECLine(char* cLine);

void vCheck1stLine(char* cLine, uint16_t iLine, uint8_t* iEnd, uint8_t *iFile);

void vCheck2ndLine(char* cLine, uint16_t iLine, uint8_t* iEnd,
										uint8_t *iFile, uint8_t *iAdd);
										
uint32_t iCountS5S6byAddress(char* Add, uint8_t* AddDec, uint32_t *count);

#endif

