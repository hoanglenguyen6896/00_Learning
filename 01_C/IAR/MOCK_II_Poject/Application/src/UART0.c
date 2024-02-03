#include "UART0.h"

/*******************************************************************************
* Global Variables
*******************************************************************************/

static uint32_t s_u32SBR; /* Variable to calculate SBR[BDH-BDL] */
static uint8_t s_u8OSR; /* Variable to calculate OSR */
static uint8_t *ptrFreeElement = NULL;
static uint16_t u16Column = 0u;

/*******************************************************************************
* Prototypes
*******************************************************************************/

/* Calculate SBR and OSR for a specific baudrate. */
static void UART0_vBaudGen(uint32_t u32Baud);
/* Send a character via UART0. */
static void UART0_vPutChar(uint8_t u8Character);

/*******************************************************************************
* Code
*******************************************************************************/



/*******************************************************************************
 * Function name: UART0_vBaudGen
 * Function: Calculate SBR and OSR for a specific baudrate.
*******************************************************************************/
static void UART0_vBaudGen(uint32_t u32Baud)
{
    uint8_t u8TempOSR = MAX_OSR_VALUE; /* OSR temporary variable */
    uint32_t u32TempSBR; /* Integer SBR temporary variable */
    uint32_t u32BaudDiff1; /* Calculate baudrate difference */
    uint32_t u32BaudDiff2; /* Calculate baudrate difference */
    uint32_t u32MinBaudDiff = 0xFFFFFFFF; /* Min baudrate difference */
    /* Initialize variable of u8OSR */
    for(u8TempOSR = MAX_OSR_VALUE; u8TempOSR >= MIN_OSR_VALUE; u8TempOSR--)
    {
        /* Calculate SBR with OSR coressponding value */
        u32TempSBR = (uint32_t) SYSTEM_CLOCK/(u32Baud*(u8TempOSR + 1u));
        if(u32TempSBR == 0u)
        {
            u32TempSBR = 1u;
        }
        /* Calculate baudrate difference with SBR coressponding value */
        u32BaudDiff1 = ((uint32_t) SYSTEM_CLOCK/(u32TempSBR*(u8TempOSR + 1u))) - u32Baud;
        /* Update s_u32SBR and u8OSR if get a better baudrate difference */
        if((u32BaudDiff1 < u32MinBaudDiff) && (u32TempSBR <= MAX_SBR_VALUE))
        {
            u32MinBaudDiff = u32BaudDiff1;
            s_u32SBR = u32TempSBR;
            s_u8OSR = (uint8_t) u8TempOSR;
        }
        u32TempSBR++;
        /* Calculate baudrate difference with SBR + 1 */
        u32BaudDiff2 = u32Baud - ((uint32_t) SYSTEM_CLOCK/(u32TempSBR*(u8TempOSR + 1u)));
        /* Update s_u32SBR and u8OSR if get a better baudrate difference */
        if((u32BaudDiff2 < u32MinBaudDiff) && (u32TempSBR <= MAX_SBR_VALUE))
        {
            u32MinBaudDiff = u32BaudDiff2;
            s_u32SBR = u32TempSBR;
            s_u8OSR = (uint8_t) u8TempOSR;
        }
    }
}

/*******************************************************************************
 * Function name: UART0_vPutChar
 * Function: Send a character via UART0.
*******************************************************************************/
static void UART0_vPutChar(uint8_t u8Character)
{
    /* Wait for Transmission Complete Flag was set (idle) */
    while(!(UART0->S1 & UART0_S1_TC_MASK));
    /* Transmit the character via UART0 */
    UART0->D = u8Character;
}

/*******************************************************************************
 * Function name: UART0_vUART0Init
 * Function: Initialize UART0
*******************************************************************************/
void UART0_vUART0Init(uint32_t u32Baudrate)
{
    /* SBR[BDH] initialize value */
    uint8_t u8BDH;
    /* SBR[BDL] initialize value */
    uint8_t u8BDL;

    UART0_vBaudGen(u32Baudrate);

    u8BDH = (s_u32SBR & SBR_BDH_MASK) >> SBR_BDH_SHIFT;
    u8BDL = (s_u32SBR & SBR_BDL_MASK);

    /* Configure clock gate for PORTA */
    SIM->SCGC5 |= SIM_SCGC5_PORTA(1u);

    /* Configure UART0 at PIN1 PIN2 of PORTA */
    PORTA->PCR[1u] &= ~PORT_PCR_MUX_MASK;
    PORTA->PCR[1u] |= PORT_PCR_MUX(UART0_MULTIPLEXING);
    PORTA->PCR[2u] &= ~PORT_PCR_MUX_MASK;
    PORTA->PCR[2u] |= PORT_PCR_MUX(UART0_MULTIPLEXING);

    /* Configure clock gate for UART0 */
    SIM->SCGC4 |= SIM_SCGC4_UART0(1u);

    /* Configure clock source for UART0 */
    SIM->SOPT2 &= ~SIM_SOPT2_UART0SRC_MASK;
    SIM->SOPT2 |= SIM_SOPT2_UART0SRC(1u);

    /* PLL/FLL clock select */
    SIM->SOPT2 &= ~SIM_SOPT2_PLLFLLSEL_MASK;

    /* Configure 8 bits data */
    UART0->C1 &= ~UART0_C1_M_MASK;
    UART0->C4 &= ~UART0_C4_M10_MASK;

    /* Configure parity bit (disable) */
    UART0->C1 &= ~UART0_C1_PE_MASK;

    /* Configure stop bit (1 bit) */
    UART0->BDH &= ~UART0_BDH_SBNS_MASK;

    /* Configure MSB or LSB first (LSB) */
    UART0->S2 &= ~UART0_S2_MSBF_MASK;

    /* Configure data polarity */
    UART0->S2 &= ~UART0_S2_RXINV_MASK;
    UART0->C3 &= ~UART0_C3_TXINV_MASK;

    /* Configure OSR */
    UART0->C4 &= ~UART0_C4_OSR_MASK;
    UART0->C4 = UART0_C4_OSR(s_u8OSR);

    /* Configure baudrate */
    UART0->BDH &= ~UART0_BDH_SBR_MASK;
    UART0->BDH |= UART0_BDH_SBR(u8BDH);
    UART0->BDL &= ~UART0_BDL_SBR_MASK;
    UART0->BDL |= UART0_BDL_SBR(u8BDL);

    /* Enable Transmitter and Reciever */
    UART0->C2 |= UART0_C2_TE(1u);
    UART0->C2 |= UART0_C2_RE(1u);

    /* Enable UART0 Interrupt */
    NVIC_EnableIRQ(UART0_IRQn);
    UART0->C2 |= UART0_C2_RIE(1u);
}


/*******************************************************************************
 * Function name: UART0_vPutChar
 * Function: Send a string via UART0.
*******************************************************************************/
void UART0_vPutString(uint8_t* u8String)
{
    uint8_t i = 0u;
    while(u8String[i] != '\0')
    {
        /* Transmit the character via UART0 ultil meet \0 */
        UART0_vPutChar(u8String[i]);
        i++;
    }
}

/*******************************************************************************
 * Function name: UART0_IRQHandler
 * Function: Handle exception of UART0.
*******************************************************************************/
void UART0_IRQHandler(void)
{
    /* Get a free row */
    while(ptrFreeElement == NULL)
    {
        ptrFreeElement = QUEUE_vGetFreeElements();
        if(ptrFreeElement == NULL)
        {
            QUEUE_vPushQ();
        }
    }

    /* Push data to queue */
    ptrFreeElement[u16Column] = UART0->D;
    /* Call push if receive \n */
    if(ptrFreeElement[u16Column] == '\n')
    {
        QUEUE_vPushQ();
        ptrFreeElement = NULL;
        u16Column = 0u;
    }
    else
    {
        u16Column++;
    }
}
