#include "BUTTON.h"

/*******************************************************************************
 * Main Function
*******************************************************************************/

uint16_t countLED1 = 0;
uint16_t countLED2 = 0;

void vSysConfig(uint32_t u32Ticks)
{
    SYST->RVR = u32Ticks - 1u;
    //SYST->CVR = 0u;
    SYST->CSR |= 7u;
}

void SysTick_Handler()
{
    countLED1++;
    countLED2++;
}

int main(void)
{
    HAL_vInit();
    vSysConfig(20971U);

    while (1)
    {
        if(countLED1 == 1000)
        {
            RED_LED_TOGGLE;
            countLED1 = 0;
        }
        if(countLED2 == 167)
        {
            GREEN_LED_TOGGLE;
            countLED2 = 0;
        }
    }
}
