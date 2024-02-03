#ifndef __INIT__
#define __INIT__

#include "MKL46Z256VLL4.h"

/* Get input status of Pin12 GPIOC (SW2) */
#define BUTTON_BOOT_STATUS          (((GPIOC->PDIR) >> 12) & 1u)
/* Get input status of Pin3 GPIOC (SW2) */
#define BUTTON_1_STATUS             (((GPIOC->PDIR) >> 3) & 1u)

#define PRESS                       0u      /* For check pressed button */
#define RELEASE                     1u      /* For check released button */

/* Delay time */
#define DELAY_1S            4200000UL
#define DELAY_250MS         1050000UL
#define DELAY_100US         420UL

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Config pin */
void GPIO_vInit(void);

#endif
