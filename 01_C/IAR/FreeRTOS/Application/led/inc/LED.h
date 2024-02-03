#ifndef __LED__
#define __LED__

#include "INIT.h"

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Blink 2 led Alternate */
void LED_vBlinkAlternate( void * pvParameters );
/* Dim 2 led Alternate */
void LED_vDimLED(uint8_t u8DutyCycle);

#endif
