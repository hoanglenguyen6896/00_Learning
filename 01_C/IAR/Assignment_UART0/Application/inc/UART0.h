#ifndef __UART0__
#define __UART0__

#include "QUEUE.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define UART0_IRQn              (12u)       /* UART0 Interrupt priority levels */

#define SYSTEM_CLOCK            (20971520u) /* Default System clock */
#define MAX_OSR_VALUE           (31u)       /* Maximun value of OSR - 5 bit */
#define MIN_OSR_VALUE           (3u)        /* Minimum value of OSR is 3u */
#define MAX_SBR_VALUE           (8191u)
#define SBR_BDL_MASK            (0xFFu)
#define SBR_BDH_MASK            (0x1F00u)
#define SBR_BDH_SHIFT           (8u)

#define UART0_MULTIPLEXING      (2u)        /* UART0 Signal Multiplexing */

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Innitialize UART0 */
void UART0_vUART0Init(uint32_t u32Baudrate);
/* Send a string via UART0 */
void UART0_vPutString(uint8_t* u8String);

#endif  /* __UART0__ */
