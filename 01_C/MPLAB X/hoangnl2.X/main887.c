#pragma config FOSC = HS        
#pragma config WDTE = OFF       
#pragma config PWRTE = OFF     
#pragma config MCLRE = ON       
#pragma config CP = OFF         
#pragma config CPD = OFF        
#pragma config BOREN = ON       
#pragma config IESO = ON        
#pragma config FCMEN = ON       
#pragma config LVP = OFF       

#pragma config BOR4V = BOR40V   
#pragma config WRT = OFF        

#define _XTAL_FREQ 11059200
#include <xc.h>
#define RS RD7
#define EN RD6
#define D4 RD5
#define D5 RD4
#define D6 RD3
#define D7 RD2

#include "LCD.h"
#include "ESP_lib.h"

void main()
{
    TRISD = 0x00; 
    int a =0;
    char revN[16], revC[16]; 
    int _revSizeN = 0, _revSizeC = 0;
    Lcd_Init();
    UART_Init(9600) ; 
     
    Lcd_Set_Cursor(1,1);
    Lcd_Print_String("Hoangnl141782");
    Lcd_Set_Cursor(2,1);
    Lcd_Print_String("ESP8266 with PIC");
    __delay_ms(1500);
    Lcd_Clear();
    
    do
    {
    Lcd_Set_Cursor(1,1);
    Lcd_Print_String("ESP not found");
    }while (!esp8266_isStarted());
    Lcd_Set_Cursor(1,1);
    Lcd_Print_String("ESP is connected");
    __delay_ms(1500);
  
    esp8266_multi();
    Lcd_Set_Cursor(2,1);
    Lcd_Print_String("Enable multiple");
    __delay_ms(1500);
    Lcd_Clear();
 
    esp8266_mode(3);
    Lcd_Set_Cursor(1,1);
    Lcd_Print_String("ESP set as Dual");
    __delay_ms(1500);
    
    esp8266_config_server();
    Lcd_Set_Cursor(2,1);
    Lcd_Print_String("ESP set as server");
    __delay_ms(1500);
    Lcd_Clear();    
    
    esp8266_config_softAP("ESP8266","12345678");
    Lcd_Set_Cursor(1,1);
    Lcd_Print_String("ID: ESP8266");
    Lcd_Set_Cursor(2,1);
    Lcd_Print_String("Pass: 12345678"); 
    __delay_ms(1500);
    Lcd_Clear();
    
    Lcd_Set_Cursor(1,1);
    Lcd_Print_String("AP configured");
    Lcd_Set_Cursor(2,1);
    Lcd_Print_String("Waiting...");
     
    while(1)
    {
        if(_esp8266_waitResponse() == 7)
        {
            for(a=0; a<16; a++)
            {
                revN[a]='\0';
                revC[a]='\0';
            }      
            Lcd_Clear();        
            do{
                Lcd_Set_Cursor(1,1);
                Lcd_Print_String("1. Nhap Ten");           
            }while(!esp8266_send("1. Ten\r\n"));
            revClient(revN, _revSizeN);
            do{     
                Lcd_Set_Cursor(2,1);
                Lcd_Print_String("2. Nhap Gia");            
            }while(!esp8266_send("2. Gia\r\n"));
            revClient(revC, _revSizeC);           
        }   
        Lcd_Clear();
        Lcd_Set_Cursor(1,1);
        Lcd_Print_String(revN);
        Lcd_Set_Cursor(2,1);
        Lcd_Print_String(revC);
    }
}
