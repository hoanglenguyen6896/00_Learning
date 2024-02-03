#ifndef UART_pic16f628a_h
#define	UART_pic16f628a_h

#include <xc.h> 
#ifdef	__cplusplus
extern "C" {
#endif /* __cplusplus */

#ifdef	__cplusplus
}
#endif /* __cplusplus */

#endif	/* XC_HEADER_TEMPLATE_H */

char UART_Init(const long int baudrate)
{
    unsigned int x = (_XTAL_FREQ/(baudrate*64)) - 1;
    TRISB1 = 1;
    TRISB2 = 1;
    TXEN = 1;
    SPEN = 1;
    TX9 = 0;
    RX9 = 0;
    SYNC = 0;
    CREN = 1;
    BRGH = 0;
    SPBRG = x;
	/*unsigned int x;
	x = (_XTAL_FREQ - baudrate*64)/(baudrate*64);
	if(x>255)
	{
		x = (_XTAL_FREQ - baudrate*16)/(baudrate*16);
		BRGH = 1;
	}
	if(x<256)
	{
        SPBRG = x;
        SYNC = 0;
        SPEN = 1;
        TRISB2 = 1;
        TRISB1 = 1;
        CREN = 1;
        TXEN = 1;
        return 1;
	}*/
	return 0;
}

char UART_TX_Empty()
{
  return TRMT;
}

char UART_Data_Ready()
{
   return RCIF;
}
char UART_Read()
{
  while(!RCIF);
  return RCREG;
}

void UART_Read_Text(char *Output, unsigned int length)
{
    unsigned int i;
    for(int i=0;i<length;i++)
        Output[i] = UART_Read();
}
void UART_Send(char data)
{
    while(!TRMT);
    TXREG = data;
}

void UART_Send_String(char *text)
{
  int i;
  for(i=0;text[i]!='\0';i++)
	  UART_Send(text[i]);
}