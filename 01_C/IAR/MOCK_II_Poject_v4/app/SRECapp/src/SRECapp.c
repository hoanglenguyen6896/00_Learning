#include "SRECapp.h"

/*******************************************************************************
 * Global Variables
*******************************************************************************/

static uint8_t *putPtr = NULL;

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: SREC_init
 * Description: Point to a free row of queue to put
*******************************************************************************/
void SRECapp_init(void)
{
    /* Get free row address */
    putPtr = QUEUE_getFreeElements();
}

/*******************************************************************************
 * Function name: SREC_vCallBack
 * Description: Callback function to put character into queue
*******************************************************************************/
void SRECapp_callback(uint8_t character)
{
    static uint16_t putIndex = 0u;
    /* put character to row */
    putPtr[putIndex++] = character;
    if(character == '\n')
    {
        /* Call queue push and get another free row of queue */
        putIndex = 0u;
        QUEUE_pushQ();
        putPtr = QUEUE_getFreeElements();
    }
}
