#include "BOOT.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/

#define INVALID_UINT32              (0xFFFFFFFFu)
#define WAIT_TIME_STABLE            (500000u)

/*******************************************************************************
 * Code
*******************************************************************************/

/*******************************************************************************
 * Funtion name: BOOT_bootloader
 * Description: Update new app or switch to app
*******************************************************************************/
void BOOT_bootloader(void)
{
    /* Local Variable defititions*/
    uint8_t *queueRowPtr = NULL; /* Point to a row of queue */
    /* Srec line's status after parsed */
    parseStatus_t LineStatus = parseStatus_start;
    parsedData_struct_t LineData; /* Data struct of a Srec line */
    uint8_t *dataPtr = NULL; /* Point to data field of line struct */
    int16_t dataLength = 0u; /* data length */
    uint16_t flashSizeInSector; /* Size of flash region for app */
    uint32_t stableTime = WAIT_TIME_STABLE; /* Delay time for stabilize board */

    /* Initialize */
    GPIO_init();
    UART0_init(BAUDRATE, SRECapp_callback);
    SRECapp_init();

    /* Wait for stable */
    while(stableTime--);

    /* Run BOOT if BOOT button is pressed or App region is empty */
    if((BUTTON_BOOT_STATUS == PRESS)\
                        || (*(uint32_t*)(APP_START_ADDR) == INVALID_UINT32))
    {
        /* Print notification */
        UART0_putString("\r\n--------------------------------------------------"
                        "---------------------------------------------------");
        UART0_putString("\r\n----------------------------------- BOOT MODE "
                        "------------------------------------------\r\n");
        UART0_putString("-----------------------------------------------------"
                        "------------------------------------------------\r\n");
        flashSizeInSector = (APP_END_ADDR - APP_START_ADDR)/SECTOR_SIZE;
        /* Delete all flash sectors of App region */
        UART0_putString("Erasing flash ...");
        __disable_irq();
        Erase_Multi_Sector(APP_START_ADDR, flashSizeInSector);
        __enable_irq();
        UART0_putString("Done!!!\r\n");
        /* Print request to send a Srec file */
        UART0_putString("Send your SREC file: ...\r\n");
        /* While parse Srec line is not error */
        while(1u)
        {
            /* Peek a row of queue */
            queueRowPtr = QUEUE_peekQ();
            /* If row is valid (not empty) */
            if(queueRowPtr != NULL)
            {
                /* parse data from queue's row */
                LineStatus = SREC_parsesrecLine(queueRowPtr, &LineData);
                /* Pop queue */
                QUEUE_popQ();
                switch(LineStatus)
                {
                    case parseStatus_start:
                    case parseStatus_optional:
                        UART0_putString(".");
                        break;
                    case parseStatus_inProgress:
                        UART0_putString(".");
                        dataPtr = LineData.data;
                        dataLength = LineData.length;
                        while(dataLength > 0u)
                        {
                            /* Write data to flash until dataLength <= 0 */
                            __disable_irq();
                            Program_LongWord_8B(LineData.address, dataPtr);
                            __enable_irq();
                            dataPtr = dataPtr + 4u;
                            LineData.address = LineData.address + 4u;
                            dataLength = dataLength - 4u;
                        }
                        break;
                    case parseStatus_end:
                    /* if write successfully into flash, print notification */
                        UART0_putString("\r\nSucceeded! Please reset your board"
                             " and release BOOT button to run your App\r\n");
                        UART0_putString("(If you want to write another SREC"
                             " file, please press SW1 (left switch))\r\n");
                        break;
                    case parseStatus_error:
                    default: /* parseStatus_error */
                        UART0_putString("Error!\r\n");
                        break;
                }
                /* if error, delete flash, request send a valid file */
                if(LineStatus == parseStatus_error)
                {
                    /* Pop all data send from terminal after error until end */
                    while((queueRowPtr[1u] != '7')\
                            && (queueRowPtr[1u] != '8')\
                                && (queueRowPtr[1u] != '9'))
                    {
                        queueRowPtr = QUEUE_peekQ();
                        QUEUE_popQ();
                    }
                    /* Erase flash */
                    UART0_putString("Erasing flash ...");
                    __disable_irq();
                    Erase_Multi_Sector(APP_START_ADDR, flashSizeInSector);
                    __enable_irq();
                    UART0_putString("Done!!!\r\n");
                    /* Request send a valid file */
                    UART0_putString("Please send a valid SREC file\r\n");
                }
            }
            /* If user want to write another Srec after succeeded */
            if(BUTTON_1_STATUS == PRESS && LineStatus == parseStatus_end)
            {
                /* Delete flash */
                UART0_putString("Erasing flash ...");
                __disable_irq();
                Erase_Multi_Sector(APP_START_ADDR, flashSizeInSector);
                __enable_irq();
                UART0_putString("Done!!!\r\n");
                /* Request send Srec file */
                UART0_putString("Send your SREC file: ...\r\n");
            }
        }
    }
    else
    {
        /* If BOOT button is not press, jump to App by Function pointer */
        uint32_t appResetAddr = *(uint32_t*) ((APP_START_ADDR + 4u));
        SwitchToAppPtr SwitcToAppFunc;
        SwitcToAppFunc = (SwitchToAppPtr) (appResetAddr);
        /* Set Vector Table Offset Register */
        SCB->VTOR = APP_START_ADDR;
        /* Set Main Stack Pointer */
        __set_MSP(*(uint32_t*)(APP_START_ADDR));
        /* Jump to app */
        SwitcToAppFunc();
    }
}
