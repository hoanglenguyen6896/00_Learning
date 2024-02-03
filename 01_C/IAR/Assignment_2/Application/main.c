#include "BUTTON.h"

/*******************************************************************************
 * Main Function
*******************************************************************************/

int main(void)
{
    uint8_t u8Mode = 0;
    uint8_t u8Brightness = BRIGHTNESS_0;

    HAL_vInit();

    while (1)
    {
        switch(u8Mode)
        {
            case (MODE_1):
                BUTTON_vCheckButtonMode1(&u8Brightness, &u8Mode);
                break;
            case (MODE_2A):
                BUTTON_vCheckButtonMode2A(&u8Brightness, &u8Mode);
                break;
            case (MODE_2B):
                BUTTON_vCheckButtonMode2B(&u8Brightness, &u8Mode);
                break;
        }
    }
}
