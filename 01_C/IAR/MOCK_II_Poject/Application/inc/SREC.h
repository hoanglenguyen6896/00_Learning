#ifndef __SREC__
#define __SREC__

#include "MKL46Z256VLL4.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define CHKSUM_MASK         (0xFFu)
#define TRUE                (1u)
#define FALSE               (0u)

typedef struct
{
    uint32_t address;
    uint8_t data[256];
    uint16_t length;
}parsedData_struct_t;

typedef enum
{
    parseStatus_start = 0,
    parseStatus_inProgress,
    parseStatus_error,
    parseStatus_end,
}parseStatus_t;

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Parse a Srec line */
parseStatus_t SREC_parseSrecLine(uint8_t *u8SrecLine,
                                            parsedData_struct_t *LineObject);

#endif  /* __UART0__ */
