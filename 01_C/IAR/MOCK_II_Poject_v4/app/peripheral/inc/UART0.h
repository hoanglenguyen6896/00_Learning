#ifndef __UART0__
#define __UART0__

#include "QUEUE.h"
#include "GPIO.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define BAUDRATE                (115200u)   /* Baudrate of UART0 */

#define UART0_MULTIPLEXING      (2u)        /* UART0 Signal Multiplexing */

typedef void (*f)(uint8_t character);

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Innitialize UART0 */
void UART0_init(uint32_t baudraterate, f callback);
/* Send a string via UART0 */
void UART0_putString(uint8_t* u8String);

#endif  /* __UART0__ */
