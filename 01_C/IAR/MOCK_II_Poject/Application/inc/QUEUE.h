#ifndef __QUEUE__
#define __QUEUE__

#include "MKL46Z256VLL4.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define QROW                (4u)    /* Max queue row */
#define QCOL                (520u)  /* Max queue column */
#define ROW_EMPTY           (0u)
#define ROW_FULL            (1u)

typedef struct
{
    uint8_t Data[QROW][QCOL];       /* Queue data */
    uint8_t ArrRowStatus[QROW];    /* Queue row status */
}Queue_Struct_t;

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Get free row of queue */
uint8_t* QUEUE_vGetFreeElements(void);
/* Peek data of queue */
uint8_t* QUEUE_vPeekQ(void);
/* Push data to queue */
void QUEUE_vPushQ(void);
/* Pop data from queue and handle it */
void QUEUE_u8PopQ(void);

#endif  /* __QUEUE__ */
