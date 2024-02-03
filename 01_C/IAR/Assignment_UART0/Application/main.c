#include "QUEUE.h"
#include "UART0.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/
#define BAUDRATE            (115200) /* Baudrate of UART0 */

/*******************************************************************************
 * Main Function
*******************************************************************************/
int main(void)
{
    /* Local Variable defititions*/
    uint8_t chk = 0u; /* Get pop status */

    /* Initialize */
    UART0_vUART0Init(BAUDRATE); /* Initialize UART0 */
    UART0_vPutString("\r\nSend your SREC file: ...\r\n"); /* Send start str */
    /* Perform check SREC until meet Error */
    while(chk != FILE_ERROR)
    {
        chk = QUEUE_u8PopQ(); /* Get pop status */
        if(chk == FILE_ERROR)
        {
            UART0_vPutString("ERROR\r\n"); /* Send Error */
        }
        else if((chk == END_OF_FILE) || (chk == LINE_VALID))
        {
            UART0_vPutString(">>\r\n"); /* Send >> */
        }
    }
}
