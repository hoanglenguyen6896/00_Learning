#ifndef __QUEUE__
#define __QUEUE__

#include "SREC.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define QROW                (4u)    /* Max queue row */
#define QCOL                (100u)  /* Max queue column */

#define LINE_FULL           (10u)    /* Line status is Full */
#define LINE_EMPTY          (11u)    /* Line status is Empty */

#define FILE_ERROR          (1u)    /* File Status is Error of Queue is full */
#define END_OF_FILE         (2u)    /* End of file */

typedef struct UART0_queue_struct
{
    uint8_t Data[QROW][QCOL];       /* Queue data */
    uint8_t u8LineStatusArr[QROW];  /* Queue row status */
    uint8_t u8LineLengthArr[QROW];  /* Queue data row length */
}QueueStruct;

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Push data to queue */
void QUEUE_vPushQ(uint8_t u8Char);
/* Pop data from queue and handle it */
uint8_t QUEUE_u8PopQ(void);

#endif  /* __QUEUE__ */
