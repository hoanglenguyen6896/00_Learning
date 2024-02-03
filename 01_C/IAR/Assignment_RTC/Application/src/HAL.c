#include "HAL.h"

/*******************************************************************************
 * Function name: HAL_vPinInit
 * Function: Config pin
*******************************************************************************/
void HAL_vPinInit(void)
{
    /* Enable clock for PORTD, PORTE */
    SIM->SCGC5 |= ((SIM_SCGC5_PORTD(1))|(SIM_SCGC5_PORTE(1)));

    /* Configure multiplex of PTD5, PTE29 as GPIO */
    PORTD->PCR[5] |= (1u << PIN_MUX_CONTROL_SHIFT);
    PORTE->PCR[29] |= (1u << PIN_MUX_CONTROL_SHIFT);

    /* Configure PTD5, PTE29 as output */
    GPIOD->PDDR |= (1u << 5u);
    GPIOE->PDDR |= (1u << 29u);

    /* Configure PTD5, PTE29 output logic is high (Turn off LED) */
    GPIOD->PSOR |= (1u << 5u);
    GPIOE->PSOR |= (1u << 29u);
}

/*******************************************************************************
 * Function name: HAL_vRTCInit
 * Function: Initialize RTC
*******************************************************************************/
void HAL_vRTCInit()
{
    /* Enable clock for RTC */
    SIM->SCGC6 |= SIM_SCGC6_RTC(1u);
    /* Configure 1kHz clock for RTC */
    SIM->SOPT1 |= SIM_SOPT1_OSC32KSEL(3u);

    /* Perform software reset */
    RTC->CR |= (1u<<0u);

    RTC->CR &= ~(1u<<0u);

    /* Initialize value for TSR and TCR */
    RTC->TSR = 1u;
    RTC->TPR = 0u;

    /* Enable time counter */
    RTC->SR |= (1u<<4u);
}