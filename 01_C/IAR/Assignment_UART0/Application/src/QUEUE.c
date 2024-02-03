#include "QUEUE.h"

/*******************************************************************************
* Global Variables
*******************************************************************************/

static QueueStruct Queue;

static uint8_t s_u8RowPush;         /* Row index to push data into queue */
static uint8_t s_u8ColPush;         /* Column index to push data into queue */
static uint8_t s_u8RowPop;          /* Row index to pop data from queue */

static uint32_t s_u32TotalDataLine; /* Total S1/2/3 line of the SREC */
static uint8_t s_u8FileChk;         /* File  status */

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: QUEUE_vPushQ
 * Function: Push data to queue
*******************************************************************************/
void QUEUE_vPushQ(uint8_t u8Char)
{
    /* If Queue is line is full (not handle yet), return file error */
    if(Queue.u8LineStatusArr[s_u8RowPush] == LINE_FULL)
    {
        s_u8FileChk = FILE_ERROR;
    }
    /* Check if recieve char is \n - end a SREC line */
    else if(u8Char == '\n')
    {
        /* Line status is FULL */
        Queue.u8LineStatusArr[s_u8RowPush] = LINE_FULL;
        /* Get line size */
        Queue.u8LineLengthArr[s_u8RowPush] = s_u8ColPush - 1u;
        if((Queue.Data[s_u8RowPop][1u] == '1')
                    || (Queue.Data[s_u8RowPop][1u] == '2')
                        || (Queue.Data[s_u8RowPop][1u] == '3'))
        {
            s_u32TotalDataLine++; /* Increase total S1/2/3 line by 1 */
        }
        s_u8RowPush = (s_u8RowPush + 1u)%QROW; /* To next row in queue */
        s_u8ColPush = 0u; /* Reset Column index */
    }
    else
    {
        /* Push character to queue */
        Queue.Data[s_u8RowPush][s_u8ColPush] = u8Char;
        s_u8ColPush++;
    }
}

/*******************************************************************************
 * Function name: QUEUE_u8PopQ
 * Function: Pop data from queue and handle it
*******************************************************************************/
uint8_t QUEUE_u8PopQ(void)
{
    uint8_t u8PopChk = LINE_EMPTY;
    /* Check if Line is EMPTY or FULL */
    if((Queue.u8LineStatusArr[s_u8RowPop] == LINE_FULL)
                                                && (s_u8FileChk != FILE_ERROR))
    {
        /* If Line is not empty, perform check line */
        u8PopChk = SREC_u8ChkSRECLine(*(Queue.Data + s_u8RowPop),
                               Queue.u8LineLengthArr[s_u8RowPop]);
        /* If line is valid SREC line */
        if(u8PopChk == LINE_VALID)
        {
            s_u8FileChk = u8PopChk;
            /* Check line count if meet S5 or S6 line */
            if((Queue.Data[s_u8RowPop][1u] == '5')
                                    || (Queue.Data[s_u8RowPop]
                                        [1u] == '6'))
            {
                u8PopChk = SREC_u8ChkLineCount(*(Queue.Data + s_u8RowPop),
                                    &s_u32TotalDataLine,
                                    Queue.u8LineLengthArr[s_u8RowPop]);
                if(u8PopChk != LINE_VALID)
                {
                    s_u8FileChk = FILE_ERROR;
                }
            }
            /* Return EOF if meet S7, S8 or S9 */
            if((Queue.Data[s_u8RowPop][1u] == '7')
                    || (Queue.Data[s_u8RowPop][1u] == '8')
                        || (Queue.Data[s_u8RowPop][1u] == '9'))
            {
                s_u8FileChk = END_OF_FILE;
                s_u32TotalDataLine = 0u;
            }
        }
        else
        {
            s_u8FileChk = FILE_ERROR;
        }
        /* After line is processed, assign FULL to line status */
        Queue.u8LineStatusArr[s_u8RowPop] = LINE_EMPTY;
        s_u8RowPop = (s_u8RowPop + 1u)%QROW;
    }
    else
    {
        s_u8FileChk = LINE_EMPTY;
    }

    return s_u8FileChk;
}
