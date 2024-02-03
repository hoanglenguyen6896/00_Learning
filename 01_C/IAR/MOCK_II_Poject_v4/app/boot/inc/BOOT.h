#ifndef __BOOT__
#define __BOOT__

#include "UART0.h"
#include "QUEUE.h"
#include "SREC.h"
#include "SRECapp.h"
#include "Flash.h"
#include "GPIO.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define APP_START_ADDR              (0x0000A000u) /* App start address */
#define APP_END_ADDR                (0x0003FFFFu) /* App end address */

typedef void (*SwitchToAppPtr)(void);

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Update new app or switch to app */
void BOOT_bootloader(void);

#endif  /* __BOOT__ */
