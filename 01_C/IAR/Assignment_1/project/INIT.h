#ifndef __INIT__
#define __INIT__

#include "MKL46Z4.h"

#define GREEN_LED_ON        GPIOD->PCOR |= (1 << 5)
#define GREEN_LED_OFF       GPIOD->PSOR |= (1 << 5)
#define RED_LED_ON          GPIOE->PCOR |= (1 << 29)
#define RED_LED_OFF         GPIOE->PSOR |= (1 << 29)

#define DELAY_1S            4200000UL
#define DELAY_250MS         1050000UL
#define DELAY_100US         420UL

#define DIM_FREQ            100U

#define TOTAL_BLINK_MODE_1  10U
#define TOTAL_BLINK_MODE_2  5U

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Config pin */
void INIT_vInitLed();
/* Create delay */
void INIT_vDelay(uint32_t u32DelayCount);

#endif
