#ifndef __BUTTON__
#define __BUTTON__

#include "LED.h"

#define PRESS                       0u      /* For check pressed button */
#define RELEASE                     1u      /* For check released button */

/* Get input status of Pin12 GPIOC (SW2) */
#define BUTTON_2_STATUS             (((GPIOC->PDIR) >> 12) & 1u)
/* Get input status of Pin3 GPIOC (SW2) */
#define BUTTON_1_STATUS             (((GPIOC->PDIR) >> 3) & 1u)

#define MODE_1                      0u      /* Mode 1 */
#define MODE_2A                     1u      /* Mode 2A */
#define MODE_2B                     2u      /* Mode 2B */

/* Perform change brightness when press SW1 */
#define PERFORM_CHANGE_BRIGHTNESS   1u
/* Dont change brightness */
#define DONOT_CHANGE_BRIGHTNESS     0u

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Get button 2 (PORTC_PIN12) status */
void BUTTON_vCheckButtonMode1(uint8_t* u8Brightness, uint8_t *u8Status2);
/* Get button 1 (PORTC_PIN3) status to increased brightness */
void BUTTON_vCheckButtonMode2A(uint8_t* u8Brightness, uint8_t *status);
/* Get button 1 (PORTC_PIN3) status to decreased brightness */
void BUTTON_vCheckButtonMode2B(uint8_t* u8Brightness, uint8_t *status);

#endif
