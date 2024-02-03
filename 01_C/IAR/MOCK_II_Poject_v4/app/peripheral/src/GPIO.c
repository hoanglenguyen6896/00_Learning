#include "GPIO.h"

/*******************************************************************************
 * Function name: GPIO_vInit
 * Description: Initialize GPIO
*******************************************************************************/
void GPIO_init(void)
{
    /* Enable clock for PORTC, PORTD, PORTE */
    SIM->SCGC5 |= SIM_SCGC5_PORTC(1u);
    //SIM->SCGC5 |= SIM_SCGC5_PORTD(1u);
    SIM->SCGC5 |= SIM_SCGC5_PORTE(1u);
    /* Configure multiplex of PTE29 as GPIO */
    PORTE->PCR[29u] &= ~PORT_PCR_MUX_MASK;
    PORTE->PCR[29u] |= PORT_PCR_MUX(1u);
    /* Configure multiplex of PTC3 and PTC12 as GPIO */
    PORTC->PCR[3u] &= ~PORT_PCR_MUX_MASK;
    PORTC->PCR[3u] |= PORT_PCR_MUX(1u);
    PORTC->PCR[12u] &= ~PORT_PCR_MUX_MASK;
    PORTC->PCR[12u] |= PORT_PCR_MUX(1u);

    /* Configure PTE29 as output */
    GPIOE->PDDR |= (1u << 29u);

    /* Configure PTC3 and PTC12 as input */
    GPIOC->PDDR &= (~(1u << 3u));
    GPIOC->PDDR &= (~(1u << 12u));

    /* Enable pull on PTC3 and PTC12 */
    PORTC->PCR[3u] |= (1u << 1u);
    PORTC->PCR[12u] |= (1u << 1u);

    /* Configure PTC3 and PTC12 as pull-up */
    PORTC->PCR[3u] |= (1u);
    PORTC->PCR[12u] |= (1u);

    /* Configure PTE29 output is high */
    GPIOE->PSOR |= (1u << 29u);
}
