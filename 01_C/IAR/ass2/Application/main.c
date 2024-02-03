#include "LED.h"

/*******************************************************************************
 * Main Function
*******************************************************************************/

uint32_t subInc(uint32_t *x)
{
//    *x+=1;
//    *x-=1;
    (*x)++;
    (*x)--;
    return *x;
}

uint32_t increase(uint32_t a)
{
    a++;
    subInc(&a);
    return a;
}

int main(void)
{
    volatile uint32_t i = 125u;
    uint32_t a = 0u;
    uint32_t b = 0u;
    volatile uint32_t a1 = 1u;
    volatile uint32_t a2 = 2u;
    int x = 0;
    INIT_vInitLed();
    RED_LED_OFF;
    GREEN_LED_OFF;
    while (1)
    {

        a = a1*a2;
        a = a2++;
        a = i + 1;
        a = increase(i);
        b = increase(a);
    }
}