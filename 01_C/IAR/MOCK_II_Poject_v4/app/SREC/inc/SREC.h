#ifndef __SREC__
#define __SREC__

#include "MKL46Z4.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define CHKSUM_MASK         (0xFFu)

/* Line data struct */
typedef struct
{
    uint32_t address;
    uint16_t length;
    uint8_t data[256];
}parsedData_struct_t;

typedef enum
{
    parseStatus_start = 0x00,
    parseStatus_inProgress,
    parseStatus_optional,
    parseStatus_error,
    parseStatus_end,
}parseStatus_t;

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Parse a Srec line */
parseStatus_t SREC_parsesrecLine(uint8_t *srecLine,
                                            parsedData_struct_t *LineObject);

#endif  /* __UART0__ */
