#ifndef _LED_
#define _LED_
/*INCLUDE***********************************************************************
 *
*END***************************************************************************/
#include "MKL46Z4.h"
/*DEFINE***********************************************************************
 *
*END***************************************************************************/
#define GREEN_LED_ON                GPIOD->PCOR |= (1 << 5)
#define GREEN_LED_OFF               GPIOD->PSOR |= (1 << 5)
#define RED_LED_ON                  GPIOE->PCOR |= (1 << 29)
#define RED_LED_OFF                 GPIOE->PSOR |= (1 << 29)

#define DELAY_COUNT                 420u
#define DUTY_CYCLE_MIN              0
#define DUTY_CYCLE_MAX              100u
#define SECOND_MODE_1               2500u
#define LIMIT_COUNT_MODE_1          10u
#define LIMIT_COUNT_MODE_2          15u
/*FUNCTION PROPOTYPE************************************************************
 *
*END***************************************************************************/
void LED_vInitLed();/* config clock and GPIO */
void LED_vMode1();
void LED_vMode2();

#endif /*end _LED_ */
/* *****************************************************************************
 * EOF
 ******************************************************************************/