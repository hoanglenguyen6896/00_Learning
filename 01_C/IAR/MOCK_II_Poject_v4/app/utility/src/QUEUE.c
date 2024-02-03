#include "QUEUE.h"

/*******************************************************************************
* Global Variables
*******************************************************************************/

uint8_t Queue[QROW][QCOL];

static uint8_t s_rowPushIndex;         /* Row index to push data into queue */
static uint8_t s_rowPopIndex;          /* Row index to pop data from queue */
static uint8_t s_queueLevel;

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: QUEUE_vGetFreeElements
 * Function: Get a free row of queue
*******************************************************************************/
uint8_t* QUEUE_getFreeElements(void)
{
    uint8_t *ptr = NULL;

    if(s_queueLevel != QUEUE_FULL)
    {
        ptr = *(Queue + s_rowPushIndex);
    }
    /* Return NULL if queue is full, free row address if not */
    return ptr;
}

/*******************************************************************************
 * Function name: QUEUE_vPeekQ
 * Function: Peek data of queue
*******************************************************************************/
uint8_t* QUEUE_peekQ(void)
{
    uint8_t *ptr = NULL;

    if(s_queueLevel != QUEUE_EMPTY)
    {
        ptr = *(Queue + s_rowPopIndex);
    }
    /* Return NULL if queue is empty, row contains data if not */
    return ptr;
}

/*******************************************************************************
 * Function name: QUEUE_vPushQ
 * Function: Push data to queue
*******************************************************************************/
void QUEUE_pushQ(void)
{
    /* Push queue if queue is not full */
    if(s_queueLevel < QUEUE_FULL)
    {
        s_queueLevel++;
        s_rowPushIndex = (s_rowPushIndex + 1u) % QROW;
    }
    else
    {
        /* Hang program here if queue overflow */
        while(1u); /* Queue overflow */
    }
}

/*******************************************************************************
 * Function name: QUEUE_u8PopQ
 * Function: Pop data from queue and handle it
*******************************************************************************/
void QUEUE_popQ(void)
{
    /* Pop queue if queue is not empty */
    if(s_queueLevel > QUEUE_EMPTY)
    {
        s_queueLevel--;
        s_rowPopIndex = (s_rowPopIndex + 1u) % QROW;
    }
}
