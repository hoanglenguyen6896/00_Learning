#include "QUEUE.h"

/*******************************************************************************
* Global Variables
*******************************************************************************/

static Queue_Struct_t Queue;

static uint8_t s_u8RowPush;         /* Row index to push data into queue */
static uint8_t s_u8RowPop;          /* Row index to pop data from queue */

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: QUEUE_vGetFreeElements
 * Function: Get a free row of queue
*******************************************************************************/
uint8_t* QUEUE_vGetFreeElements(void)
{
    uint8_t *ptr = NULL;

    /* Check row status */
    if(Queue.ArrRowStatus[s_u8RowPush] == ROW_EMPTY)
    {
        ptr = *(Queue.Data + s_u8RowPush);
    }

    return ptr;
}

/*******************************************************************************
 * Function name: QUEUE_vPeekQ
 * Function: Peek data of queue
*******************************************************************************/
uint8_t* QUEUE_vPeekQ(void)
{
    uint8_t *ptr = NULL;

    /* Peek a full row (has data) */
    if(Queue.ArrRowStatus[s_u8RowPop] == ROW_FULL)
    {
        ptr = *(Queue.Data + s_u8RowPop);
    }

    return ptr;
}

/*******************************************************************************
 * Function name: QUEUE_vPushQ
 * Function: Push data to queue
*******************************************************************************/
void QUEUE_vPushQ(void)
{
    Queue.ArrRowStatus[s_u8RowPush] = ROW_FULL;
    s_u8RowPush = (s_u8RowPush + 1u) % QROW;
}

/*******************************************************************************
 * Function name: QUEUE_u8PopQ
 * Function: Pop data from queue and handle it
*******************************************************************************/
void QUEUE_u8PopQ(void)
{
    Queue.ArrRowStatus[s_u8RowPop] = ROW_EMPTY;
    s_u8RowPop = (s_u8RowPop + 1u) % QROW;
}
