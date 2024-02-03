
#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator: High-speed crystal/resonator on RA6/OSC2/CLKOUT and RA7/OSC1/CLKIN)
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled)
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config MCLRE = ON       // RA5/MCLR/VPP Pin Function Select bit (RA5/MCLR/VPP pin function is MCLR)
#pragma config BOREN = OFF       // Brown-out Detect Enable bit (BOD enabled)
#pragma config LVP = OFF        // Low-Voltage Programming Enable bit (RB4/PGM pin has PGM function, low-voltage programming enabled)
#pragma config CPD = OFF        // Data EE Memory Code Protection bit (Data memory code protection off)
#pragma config CP = OFF         // Flash Program Memory Code Protection bit (Code protection off)
#include <xc.h>
#define _XTAL_FREQ 8000000

#define RS PORTBbits.RB3
#define EN PORTBbits.RB4
#define D4 PORTAbits.RA3
#define D5 PORTAbits.RA2
#define D6 PORTAbits.RA1
#define D7 PORTAbits.RA0
#include "LCD.h"
//#include "ESP8266_pic16f628a.h"

main() 
{
    TRISA3=0; RA3=0;
    TRISA2=0; RA2=0;
    TRISA1=0; RA1=0;
    TRISA0=0; RA0=0;
    TRISB3=0; RB3=0;
    TRISB4=0; RB4=0;
    Lcd_Init();
    while(1)       
    {
        //PORTA=~PORTA;
        Lcd_Clear();       
        Lcd_Set_Cursor(1,1);
        Lcd_Print_String("1234567890");
        Lcd_Set_Cursor(2,1);
        Lcd_Print_String("Project III");
        __delay_ms(1000);
    }
    return 1;
}