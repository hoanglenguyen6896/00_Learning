#include "HAL.h"

/*******************************************************************************
 * Function name: HAL_vPinInit
 * Function: Config pin
*******************************************************************************/
void HAL_vPinInit(void)
{
    /* Enable clock for PORTD, PORTE */
    SIM->SCGC5 |= ((CLOCKD_ENABLE)|(CLOCKE_ENABLE));

    /* Configure multiplex of PTD5, PTE29 as GPIO */
    PORTD->PCR[5] |= (1 << PIN_MUX_CONTROL_SHIFT);
    PORTE->PCR[29] |= (1 << PIN_MUX_CONTROL_SHIFT);

    /* Configure PTD5, PTE29 as output */
    GPIOD->PDDR |= (1 << 5);
    GPIOE->PDDR |= (1 << 29);

    /* Configure PTD5, PTE29 output logic is high (Turn off LED) */
    GPIOD->PSOR |= (1 << 5);
    GPIOE->PSOR |= (1 << 29);
}

/*******************************************************************************
 * Function name: HAL_vSysConfig
 * Function: Create system timer
*******************************************************************************/
uint8_t HAL_vSysConfig(uint32_t u32Ticks)
{
    /* Checking function parameter */
    uint8_t u8SysParaError = 0u;

    if((u32Ticks - 1u) > SYSTICK_MAX_RELOAD_VALUE) /* If error */
    {
        u8SysParaError = 1u;
    }
    /* Load value into Reload Value Register */
    SYST->RVR = u32Ticks - 1u;
    /* Enable processor clock, exception, enable systick */
    SYST->CSR |= (CLKSRC_ENABLE | TICKINT_ENABLE | SYST_ENABLE);

    return u8SysParaError;
}
