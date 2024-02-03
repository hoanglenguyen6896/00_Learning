#ifndef __LED__
#define __LED__

#include "HAL.h"

#define STEP_BRIGHTNESS             25u     /* Brightness change each step */
#define BRIGHTNESS_0                0u      /* Brightness is 0/turn off */
#define BRIGHTNESS_25               25u     /* Brightness is 25 */
#define BRIGHTNESS_75               75u     /* Brightness is 75 */
#define BRIGHTNESS_100              100u    /* Brightness is 100/brightess */

/* Output logic 0 at Pin 29 GPIOE (Turn red led on) */
#define RED_LED_ON          GPIOE->PCOR |= (1 << 29)
/* Output logic 1 at Pin 29 GPIOE (Turn red led off)*/
#define RED_LED_OFF         GPIOE->PSOR |= (1 << 29)

#define TRUE                        1u
#define FALSE                       0u

#define REVERSE_DIRECTION           100u     /* Change LED dim direction */

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Bright the LED in step 0 25 50 75 100% */
void LED_vStepLED(uint8_t u8Brightness);
/* Dim the LED from 0 - 100 and 100 - 0 in 2s, 100Hz */
void LED_vDimLED(void);

#endif
