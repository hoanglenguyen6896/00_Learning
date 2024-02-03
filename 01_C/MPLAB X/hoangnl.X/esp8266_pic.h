//Define const
#define 
#define Station 1
#define AP      2
#define Dual    3

//Function here
char UART_Init(const long int); //Setup

void _esp8266_putch(unsigned char);
unsigned char _esp8266_getch(void);

void _esp8266_print(unsigned const char); //Send a string to ESP

//Code
char UART_Init(const long int baudrate)
{
    unsigned int x;
    x = (_XTAL_FREQ - baudrate*64)/(baudrate*64);       //SPBRG for Low Baud Rate
    if(x>255)                                           //If High Baud Rage Required
    {
        x = (_XTAL_FREQ - baudrate*16)/(baudrate*16);   //SPBRG for High Baud Rate
        BRGH = 1;                                       //Setting High Baud Rate
    }
    if(x<256)
    {
        SPBRG = x;                                      //Writing SPBRG Register
        SYNC = 0;                                       //Setting Asynchronous Mode, ie UART
        SPEN = 1;                                       //Enables Serial Port
        TRISC7 = 1;                                     //As Prescribed in Datasheet
        TRISC6 = 1;                                     //As Prescribed in Datasheet
        CREN = 1;                                       //Enables Continuous Reception
        TXEN = 1;                                       //Enables Transmission
        return 1;                                       //Returns 1 to indicate Successful Completion
    }
  return 0;                                             //Returns 0 to indicate UART initialization failed
}
//-----------------------------------------------------------------------------------------------------------
char _esp8266_getch(){          //Function to get one byte of date from UART
    if(OERR){                   // check for Error 
        CREN = 0;               //If error -> Reset 
        CREN = 1;               //If error -> Reset 
    }
    while(!RCIF);               // hold the program till RX buffer is free    
    return RCREG;               //receive the value and send it to main function
}
//-----------------------------------------------------------------------------------------------------------
void _esp8266_putch(char bt){   //Function to send one byte of date to UART
    while(!TXIF);               // hold the program till TX buffer is free
    TXREG = bt;                 //Load the transmitter buffer with the received value
}
//-----------------------------------------------------------------------------------------------------------
/*Output a string to the ESP module.
 * This is a function for internal use only.
 * @param ptr A pointer to the string to send.*/
void _esp8266_print(unsigned const char *ptr) {
    while (*ptr != 0) {
        _esp8266_putch(*ptr++);
    }
}
//-----------------------------------------------------------------------------------------------------------