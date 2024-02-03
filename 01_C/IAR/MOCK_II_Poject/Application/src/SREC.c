#include "SREC.h"

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Convert char to number */
static uint8_t SREC_u8HexConverter(uint8_t u8Char);

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: SREC_u8CharToNumber
 * Description: Convert char to number
*******************************************************************************/
static uint8_t SREC_u8HexConverter(uint8_t u8Char)
{
    uint8_t u8HexValue = 0xFFu;
    if((u8Char >= '0') && (u8Char <= '9'))
    {
        u8HexValue = u8Char - '0';
    }
    else if((u8Char >= 'A') && (u8Char <= 'F'))
    {
        u8HexValue = u8Char - 'A' + 10u;
    }

    return u8HexValue;
}

/*******************************************************************************
 * Function name: SREC_parseSrecLine
 * Description: Parse a Srec line
*******************************************************************************/
parseStatus_t SREC_parseSrecLine(uint8_t *u8SrecLine,
                                            parsedData_struct_t *LineObject)
{
    parseStatus_t lineStatus = parseStatus_error; /* Line return status after parse */
    uint8_t u8SrecType; /* Srecord type */
    uint8_t u8ByteCount; /* Byte count of a Srec line */
    uint32_t u32Addr = 0u; /* Address of a Srec line */
    uint8_t u8NumberOfAddrByte; /* Number of Address byte in a Srec line */
    uint8_t u8DataTmp;
    uint16_t u16DataIndex;
    uint8_t u8DataOffset = 4u; /* Data offset (Stype(2hexChar) + ByteCount(2hexChar) */
    uint8_t u8ChkSum = 0u; /* Checksum */

    /* Check Char[0] and get Srecord type */
    if(u8SrecLine[0u] == 'S')
    {
        u8SrecType = SREC_u8HexConverter(u8SrecLine[1u]);
        switch(u8SrecType)
        {
            case 0u:
                lineStatus = parseStatus_start;
                break;
            case 1u:
            case 2u:
            case 3u:
                lineStatus = parseStatus_inProgress;
                u8NumberOfAddrByte = u8SrecType + 1u;
                break;
            case 4u:
                lineStatus = parseStatus_error;
                break;
            case 5u:
            case 6u:
                /* Optional, in MOCK, I skip check line count */
                lineStatus = parseStatus_inProgress;
                u8NumberOfAddrByte = u8SrecType - 3u;
                break;
            case 7u:
            case 8u:
            case 9u:
                lineStatus = parseStatus_end;
                u8NumberOfAddrByte = 11u - u8SrecType;
                break;
            default:
                lineStatus = parseStatus_error;
                break;
        }
    }
    /* If the Srecord type is not error, check checksum and get data, data length and address */
    if((lineStatus == parseStatus_inProgress) || (lineStatus == parseStatus_end))
    {
        /* Get Byte count */
        u8ByteCount = (uint8_t) ((SREC_u8HexConverter(u8SrecLine[2u]) << 4u)
                        | (SREC_u8HexConverter(u8SrecLine[3u])));
        u8ChkSum += u8ByteCount;
        /* Get data */
        for(u16DataIndex = 0u; u16DataIndex < u8NumberOfAddrByte; u16DataIndex++)
        {
            u8DataTmp = (uint8_t) ((SREC_u8HexConverter(u8SrecLine[u8DataOffset]) << 4u)
                        | (SREC_u8HexConverter(u8SrecLine[u8DataOffset + 1u])));
            u32Addr = (u32Addr << 8u) | u8DataTmp;
            u8ChkSum += u8DataTmp;
            u8DataOffset += 2u;
        }
        LineObject->address = u32Addr;
        /* Get Data length */
        LineObject->length = u8ByteCount - u8NumberOfAddrByte - 1u; /* 1 byte chksum */
        for(u16DataIndex = 0u; u16DataIndex < LineObject->length; u16DataIndex++)
        {
            u8DataTmp = (uint8_t) ((SREC_u8HexConverter(u8SrecLine[u8DataOffset]) << 4u)
                        | (SREC_u8HexConverter(u8SrecLine[u8DataOffset + 1u])));
            LineObject->data[u16DataIndex] = u8DataTmp;
            u8DataOffset += 2u;
            u8ChkSum += u8DataTmp;
        }
        /* Get and check check sum */
        u8ChkSum += (uint8_t) ((SREC_u8HexConverter(u8SrecLine[u8DataOffset]) << 4u)
                        | (SREC_u8HexConverter(u8SrecLine[u8DataOffset + 1u])));
        if(u8ChkSum != 0xFFu)
        {
            lineStatus = parseStatus_error;
        }
    }

    return lineStatus;
}
