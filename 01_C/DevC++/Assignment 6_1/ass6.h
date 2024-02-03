#ifndef      __A_LL__
#define      __A_LL__

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static void ass6_printError(uint8_t isValid);

static uint8_t ass6_checkValue(uint8_t iValue, uint8_t *iValPos,\
														uint8_t *iValPrePos);

static uint8_t ass6_checkPosition(uint8_t iPosition);

void ass6_enterElement(void);

void ass6_deleteElements(void);

static void ass6_displayNormal(void);

static void ass6_displayNormal1(void);

static void ass6_displaySortUp(void);

void ass6_displayArray(void);

#endif

