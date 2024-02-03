#ifndef __QUEUE__
#define __QUEUE__

#include "MKL46Z4.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define QROW                (4u)    /* Max queue row */
#define QCOL                (518u)  /* Max queue column */
#define QUEUE_EMPTY         (0u)
#define QUEUE_FULL          (QROW - 1u)

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Get free row of queue */
uint8_t* QUEUE_getFreeElements(void);
/* Peek data of queue */
uint8_t* QUEUE_peekQ(void);
/* Push data to queue */
void QUEUE_pushQ(void);
/* Pop data from queue and handle it */
void QUEUE_popQ(void);

#endif  /* __QUEUE__ */
