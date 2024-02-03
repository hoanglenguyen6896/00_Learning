#include "SREC.h"

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Convert char to number */
static uint8_t SREC_u8CharToNumber(uint8_t u8Num);
/* Check character of SREC line */
static uint8_t SREC_u8ChkChar(uint8_t* u8Line, uint8_t Length);
/* Check Byte Count of SREC line */
static uint8_t SREC_ChkByteCount(uint8_t* u8Line, uint8_t Length);
/* Check Checksum of SREC line */
static uint8_t SREC_ChkSum(uint8_t* u8Line, uint8_t Length);

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: SREC_u8CharToNumber
 * Function: Convert char to number
*******************************************************************************/
static uint8_t SREC_u8CharToNumber(uint8_t u8Num)
{
    if(((u8Num) >= '0') && ((u8Num) <= '9'))
    {
        u8Num = u8Num - '0'; /* If char is number */
    }
    else
    {
        u8Num = u8Num - 'A' + 10u; /* If char is hex character */
    }

    return u8Num;
}

/*******************************************************************************
 * Function name: SREC_u8ChkChar
 * Function: Check character of SREC line
*******************************************************************************/
static uint8_t SREC_u8ChkChar(uint8_t* u8Line, uint8_t Length)
{
    uint8_t u8CharFlag; /* Character flag */
    uint8_t i;

    /* Check number of elements in a line is even or odd */
    if((Length%2u) == TRUE)
    {
        u8CharFlag = LINE_ERROR;
    }
    /* If number of elements is even, check 0th element is S or not */
    else if(u8Line[0u] != 'S')
    {
        u8CharFlag = LINE_ERROR;
    }
    /* Check 1st elements is 1-3 or 6-9 or not */
    else if((u8Line[1u] == 4) || (u8Line[1u] > '9') || (u8Line[1u] <'0'))
    {
        u8CharFlag = LINE_ERROR;
    }
    /* Check the other elements is hexa character or not */
    else
    {
        for(i = 2u; i < Length; i++)
        {
            if(u8Line[i] >= '0' && u8Line[i] <= '9')
            {
                u8CharFlag = LINE_VALID; /* Check number */
            }
            else if(u8Line[i] >= 'A' && u8Line[i] <= 'F')
            {
                u8CharFlag = LINE_VALID; /* Check hexa character */
            }
            else
            {
                u8CharFlag = LINE_ERROR;
            }
        }
    }

    return u8CharFlag;
}

/*******************************************************************************
 * Function name: SREC_ChkByteCount
 * Function: Check Byte Count of SREC line
*******************************************************************************/
static uint8_t SREC_ChkByteCount(uint8_t* u8Line, uint8_t Length)
{
    uint8_t u8ByteCount; /* Get Byte Count */
    uint8_t u8ByteFlag; /* Byte Count Flag */

    /* Calculate Byte Count */
    u8ByteCount = (SREC_u8CharToNumber(u8Line[2u])<<4)\
                                            | SREC_u8CharToNumber(u8Line[3u]);
    if(u8ByteCount < 3u)
    {
        u8ByteFlag = LINE_ERROR; /* A line is have more than 2 byte */
    }
    else if(u8ByteCount  != ((Length - 4u)/2u))
    {
        u8ByteFlag = LINE_ERROR; /* Check byte count */
    }
    else
    {
        u8ByteFlag = LINE_VALID;
    }

    return u8ByteFlag;
}

/*******************************************************************************
 * Function name: SREC_ChkSum
 * Function: Check Checksum of SREC line
*******************************************************************************/
static uint8_t SREC_ChkSum(uint8_t* u8Line, uint8_t Length)
{
    uint8_t u8ChkSum;
    uint32_t u32Sum = 0u;
    uint8_t u8ChkSumFlag;
    uint8_t i = 0;

    /* Calculate Sum of Byte Count, Address, Data */
    for(i=2u; i<Length; i+=2)
    {
        u32Sum += (SREC_u8CharToNumber(u8Line[i])<<4)\
                                         | SREC_u8CharToNumber(u8Line[i + 1u]);
    }
    /* Get last 8 bits */
    u8ChkSum = u32Sum & CHKSUM_MASK;
    /* Check if Checksum is valid or not */
    if(u8ChkSum == CHKSUM_MASK)
    {
        u8ChkSumFlag = LINE_VALID;
    }
    else
    {
        u8ChkSumFlag = LINE_ERROR;
    }

    return u8ChkSumFlag;
}

/*******************************************************************************
 * Function name: SREC_u8ChkSRECLine
 * Function: Check a SREC line is valid or error
*******************************************************************************/
uint8_t SREC_u8ChkSRECLine(uint8_t* u8Line, uint8_t Length)
{
    uint8_t u8ChkLineFlag = LINE_VALID; /* Line status */

    /* Check character */
    if(SREC_u8ChkChar(u8Line, Length) == LINE_ERROR)
    {
        u8ChkLineFlag = LINE_ERROR;
    }
    /* Check Byte Count */
    else if(SREC_ChkByteCount(u8Line, Length) == LINE_ERROR)
    {
        u8ChkLineFlag = LINE_ERROR;
    }
    /* Check Checksum */
    else if(SREC_ChkSum(u8Line, Length) == LINE_ERROR)
    {
        u8ChkLineFlag = LINE_ERROR;
    }

    return u8ChkLineFlag;
}

/*******************************************************************************
 * Function name: SREC_u8ChkLineCount
 * Function: Check line count from S5/S6 of SREC file
*******************************************************************************/
uint8_t SREC_u8ChkLineCount(uint8_t* u8Line, uint32_t* u8LineCount,
                            uint8_t Length)
{
    uint32_t s_u32Sum = 0u; /* Get total line in S5/S6 line*/
    uint8_t u8LineFlag; /* Check Line count flag */
    uint8_t i = 0u;

    /* Get total line count from S5/S6 line */
    for(i = Length - 3u; i > 3; i--)
    {
        s_u32Sum |= (SREC_u8CharToNumber(u8Line[i])<<(4u*(Length - i - 3u)));
    }
    /* Compare with total S1/2/3 count from UART0 */
    if(s_u32Sum == *u8LineCount)
    {
        u8LineFlag = LINE_VALID;
    }
    else
    {
        u8LineFlag = LINE_ERROR;
    }

    return u8LineFlag;
}
