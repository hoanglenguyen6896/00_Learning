#include "UART0.h"
#include "QUEUE.h"
#include "SREC.h"
#include "Flash.h"
#include "GPIO.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define APP_START_ADDRESS           (0x0000A000u)

/*******************************************************************************
 * Global Variables
*******************************************************************************/
typedef void (*Reset)(void);
//uint8_t (*sectorErase)(uint32_t addr) = Erase_Sector; //For Test

/*******************************************************************************
 * Main Function
*******************************************************************************/
int main(void)
{
    /* Local Variable defititions*/
    uint8_t *ptrLine = NULL;
    parseStatus_t LineStatus = parseStatus_start;
    parsedData_struct_t LineData;
    uint8_t eraseFlash = true;
    uint32_t u32SectorAddrDeleted = APP_START_ADDRESS;
    uint8_t *dataPtr = NULL;
    int16_t dataLength = 0u;
    uint8_t dataIndex = 0u;

    /* Initialize */
    GPIO_vInit();
    UART0_vUART0Init(BAUDRATE); /* Initialize UART0 */

    /* Hard erase flash */

    if(BUTTON_BOOT_STATUS == PRESS)
    {
        if(eraseFlash == true)
        {
            UART0_vPutString("Erasing flash ...");
            Erase_Sector(0xA000u);
            Erase_Sector(0xA400u);
            Erase_Sector(0xA800u);
            UART0_vPutString("Done!!!\r\n");
            eraseFlash = false;
        }
        UART0_vPutString("\r\nSend your SREC file: ...\r\n"); /* Send start str */
        while((LineStatus != parseStatus_error) && (LineStatus != parseStatus_end))
        {
            ptrLine = QUEUE_vPeekQ();
            if(ptrLine != NULL)
            {
                LineStatus = SREC_parseSrecLine(ptrLine, &LineData);
//                if((LineData.address - u32SectorAddrDeleted) > SECTOR_SIZE)
//                {
//                    u32SectorAddrDeleted = LineData.address;
//                    eraseFlash = true;
//                }
                if(LineStatus != parseStatus_error)
                {

                    UART0_vPutString(">>\r\n");
                    dataPtr = LineData.data;
                    dataLength = LineData.length;
                    if(LineStatus == parseStatus_inProgress)
                    {
                        while(dataLength > 0)
                        {
                            if(dataLength < 4)
                            {
                                for(dataIndex = 3u; dataIndex >= dataLength; dataIndex--)
                                {
                                    dataPtr[dataIndex] = 0xFFu;
                                }
                            }
                            Program_LongWord_8B(LineData.address, dataPtr);
                            dataPtr = dataPtr + 4u;
                            LineData.address = LineData.address + 4u;
                            dataLength = dataLength - 4;
                        }
                    }
                }
                else
                {
                    UART0_vPutString("Error\r\n");
                }
                QUEUE_u8PopQ();
            }

        }
        if(LineStatus == parseStatus_end)
        {
            UART0_vPutString("Succeeded! Please reset your board "
                             "and release BOOT button\r\n");
        }
        else
        {
            UART0_vPutString("Error! Reset your board "
                             "and push BOOT button to load APP\r\n");
        }
    }
    else
    {
        uint32_t *u32AppResetAddr = (uint32_t*) ((APP_START_ADDRESS + 4u));
        Reset myReset;
        myReset = (Reset) (*u32AppResetAddr);
        SCB->VTOR = APP_START_ADDRESS;
        myReset();

//        SCB->VTOR = APP_START_ADDRESS;
//        __asm("LDR R0, =0x0000A000u");
//        __asm("LDR R0, [R0,#4]");
//        __asm("BX R0");
    }

}
