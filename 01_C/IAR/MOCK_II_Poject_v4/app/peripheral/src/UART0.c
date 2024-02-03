#include "UART0.h"

/*******************************************************************************
* Definition
*******************************************************************************/

#define SYSTEM_CLOCK            (20971520u) /* Default System clock */
#define MAX_OSR_VALUE           (31u)       /* Maximun value of OSR - 5 bit */
#define MIN_OSR_VALUE           (3u)        /* Minimum value of OSR is 3u */
#define MAX_SBR_VALUE           (8191u)
#define SBR_BDL_MASK            (0xFFu)
#define SBR_BDH_MASK            (0x1F00u)
#define SBR_BDH_SHIFT           (8u)

/*******************************************************************************
* Global Variables
*******************************************************************************/

static uint32_t s_SBR; /* Variable to calculate SBR[BDH-BDL] */
static uint8_t s_OSR; /* Variable to calculate OSR */
static f s_callback = NULL;

/*******************************************************************************
* Prototypes
*******************************************************************************/

/* Calculate SBR and OSR for a specific baudrate. */
static void UART0_BaudGenerate(uint32_t baudrate);
/* Send a character via UART0. */
static void UART0_PutChar(uint8_t character);

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: UART0_vBaudGen
 * Function: Calculate SBR and OSR for a specific baudrate.
*******************************************************************************/
static void UART0_BaudGenerate(uint32_t baudrate)
{
    uint8_t tempOSR = MAX_OSR_VALUE; /* OSR temporary variable */
    uint32_t tempSBR; /* Integer SBR temporary variable */
    uint32_t baudrateDiff1; /* Calculate baudrate difference */
    uint32_t baudrateDiff2; /* Calculate baudrate difference */
    uint32_t ninBaudDiff = 0xFFFFFFFF; /* Min baudrate difference */
    /* Initialize variable of u8OSR */
    for(tempOSR = MAX_OSR_VALUE; tempOSR >= MIN_OSR_VALUE; tempOSR--)
    {
        /* Calculate SBR with OSR coressponding value */
        tempSBR = (uint32_t) SYSTEM_CLOCK/(baudrate*(tempOSR + 1u));
        if(tempSBR == 0u)
        {
            tempSBR = 1u;
        }
        /* Calculate baudrate difference with SBR coressponding value */
        baudrateDiff1 = ((uint32_t) SYSTEM_CLOCK/(tempSBR*(tempOSR + 1u)))\
                                                                    - baudrate;
        /* Update s_SBR and u8OSR if get a better baudrate difference */
        if((baudrateDiff1 < ninBaudDiff) && (tempSBR <= MAX_SBR_VALUE))
        {
            ninBaudDiff = baudrateDiff1;
            s_SBR = tempSBR;
            s_OSR = (uint8_t) tempOSR;
        }
        tempSBR++;
        /* Calculate baudrate difference with SBR + 1 */
        baudrateDiff2 = baudrate\
            - ((uint32_t) SYSTEM_CLOCK/(tempSBR*(tempOSR + 1u)));
        /* Update s_SBR and u8OSR if get a better baudrate difference */
        if((baudrateDiff2 < ninBaudDiff) && (tempSBR <= MAX_SBR_VALUE))
        {
            ninBaudDiff = baudrateDiff2;
            s_SBR = tempSBR;
            s_OSR = (uint8_t) tempOSR;
        }
    }
}

/*******************************************************************************
 * Function name: UART0_vPutChar
 * Function: Send a character via UART0.
*******************************************************************************/
static void UART0_PutChar(uint8_t character)
{
    /* Wait for Transmission Complete Flag was set (idle) */
    while(!(UART0->S1 & UART0_S1_TC_MASK));
    /* Transmit the character via UART0 */
    UART0->D = character;
}

/*******************************************************************************
 * Function name: UART0_vUART0Init
 * Function: Initialize UART0
*******************************************************************************/
void UART0_init(uint32_t baudraterate, f callback)
{
    /* SBR[BDH] initialize value */
    uint8_t BDH;
    /* SBR[BDL] initialize value */
    uint8_t BDL;

    UART0_BaudGenerate(baudraterate);

    BDH = (s_SBR & SBR_BDH_MASK) >> SBR_BDH_SHIFT;
    BDL = (s_SBR & SBR_BDL_MASK);

    /**/
    s_callback = callback;
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
    UART0->C4 = UART0_C4_OSR(s_OSR);

    /* Configure baudrate */
    UART0->BDH &= ~UART0_BDH_SBR_MASK;
    UART0->BDH |= UART0_BDH_SBR(BDH);
    UART0->BDL &= ~UART0_BDL_SBR_MASK;
    UART0->BDL |= UART0_BDL_SBR(BDL);

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
void UART0_putString(uint8_t* str)
{
    uint8_t index = 0u;
    while(str[index] != '\0')
    {
        /* Transmit the character via UART0 ultil meet \0 */
        UART0_PutChar(str[index]);
        index++;
    }
}

/*******************************************************************************
 * Function name: UART0_IRQHandler
 * Function: Handle exception of UART0.
*******************************************************************************/
void UART0_IRQHandler(void)
{
    uint8_t character = UART0->D;
    /* Put char to queue by callback functions */
    s_callback(character);
}
