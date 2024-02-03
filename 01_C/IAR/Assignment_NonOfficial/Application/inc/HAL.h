#ifndef __INIT__
#define __INIT__

#include "MKL46Z256VLL4.h"

/* Delay time */
#define DELAY_1S            4200000UL
#define DELAY_250MS         1050000UL
#define DELAY_100US         420UL

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Config pin */
void HAL_vInit(void);
/* Create delay */
void HAL_vDelay(uint32_t u32DelayCount);

#endif
