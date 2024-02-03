#ifndef __INIT__
#define __INIT__

#include "MKL46Z4.h"

/* Get input status of Pin12 GPIOC (SW2) (Right sw on board) */
#define BUTTON_BOOT_STATUS          (((GPIOC->PDIR) >> 12u) & 1u)
/* Get input status of Pin3 GPIOC (SW2) (Left sw on board) */
#define BUTTON_1_STATUS             (((GPIOC->PDIR) >> 3u) & 1u)
/* Press status */
#define PRESS                       0u      /* For check pressed button */

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Initialize GPIO */
void GPIO_init(void);

#endif
