#ifndef __INIT__
#define __INIT__

#include "MKL46Z256VLL4.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/
/* Turn Green LED on */
#define GREEN_LED_ON        GPIOD->PCOR |= (1 << 5u)
/* Turn Green LED off */
#define GREEN_LED_OFF       GPIOD->PSOR |= (1 << 5u)
/* Turn Red LED on */
#define RED_LED_ON          GPIOE->PCOR |= (1 << 29u)
/* Turn Red LED off */
#define RED_LED_OFF         GPIOE->PSOR |= (1 << 29u)

#define LED_IS_ON           1u
#define LED_IS_OFF          0u

#define DEFAULT_TSR         32.768

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Config pin */
void HAL_vPinInit(void);
/* Innitialize RTC */
void HAL_vRTCInit();

#endif
