#ifndef __SREC__
#define __SREC__

#include "MKL46Z256VLL4.h"
#include "string.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/
#define CHKSUM_MASK         (0xFFu)
#define TRUE                (1u)
#define FALSE               (0u)
#define LINE_ERROR          (255u)      /* Line error status */
#define LINE_VALID          (254u)      /* Line valid status */

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Check a SREC line is valid or error */
uint8_t SREC_u8ChkSRECLine(uint8_t* u8Line, uint8_t Length);
/* Check line count from S5/S6 of SREC file */
uint8_t SREC_u8ChkLineCount(uint8_t* u8Line, uint32_t* u8LineCount,
                            uint8_t Length);

#endif  /* __UART0__ */
