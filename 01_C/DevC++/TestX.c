#include <stdio.h>
#include <stdint.h>

typedef struct
{
    uint32_t address;
    uint8_t data[256];
    uint16_t length;
}parsedData_struct_t;

typedef enum
{
    parseStatus_start = 0,
    parseStatus_inProgress,
    parseStatus_error,
    parseStatus_end,
    parseStatus_idle,
}parseStatus_t;
static uint8_t SREC_u8HexConverter(uint8_t u8Char)
{
    if((u8Char >= '0') && (u8Char <= '9'))
    {
        u8Char = u8Char - '0';
    }
    else if((u8Char >= 'A') && (u8Char <= 'F'))
    {
        u8Char = u8Char - 'A' + 10u;
    }
    else
    {
        u8Char = 0xFFu;
    }

    return u8Char;
}

parseStatus_t SREC_parseSrecLine(uint8_t *u8SrecLine,
                                            parsedData_struct_t *LineObject)
{
    parseStatus_t lineStatus = parseStatus_error;
    uint8_t u8SrecType;
    uint8_t u8ByteCount;
    uint8_t u8NumberOfAddrByte;
    uint32_t u32Addr = 0u;
    uint8_t u8AddrTmp;
    uint8_t u8AddrIndex;
    uint8_t u8DataOffset = 4u;
    uint8_t u8ChkSum = 0u;
    uint8_t u8DataTmp;
    uint16_t u16DataIndex;

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
                u8NumberOfAddrByte = u8SrecType + 1;
                break;
            case 4u:
                lineStatus = parseStatus_error;
                break;
            case 5u:
            case 6u:
                lineStatus = parseStatus_inProgress;
                u8NumberOfAddrByte = u8SrecType - 3u;
                break;
            case 7u:
            case 8u:
            case 9u:
                lineStatus = parseStatus_end;
                u8NumberOfAddrByte = 11 - u8SrecType;
                break;
            default:
                lineStatus = parseStatus_error;
                break;
        }
    }
    if(lineStatus != parseStatus_error)
    {
        /* Get Byte count */
        u8ByteCount = (uint8_t) SREC_u8HexConverter(u8SrecLine[2u]) << 4u
                        | SREC_u8HexConverter(u8SrecLine[3u]);
        u8ChkSum += u8ByteCount;
        /* Get data */
        for(u8AddrIndex = 0u; u8AddrIndex < u8NumberOfAddrByte; u8AddrIndex++)
        {
            u8AddrTmp = ((SREC_u8HexConverter(u8SrecLine[u8DataOffset]) << 4u)
                        | (SREC_u8HexConverter(u8SrecLine[u8DataOffset + 1u])));
            u32Addr = (u32Addr << 8u) | u8AddrTmp;
            u8ChkSum += u8AddrTmp;
            u8DataOffset += 2u;
        }
        LineObject->address = u32Addr;
        /* Data length = Bytecount - NumberByteAddr - 1 byte chksum */
        LineObject->length = u8ByteCount - u8NumberOfAddrByte - 1u;
        for(u16DataIndex = 0u; u16DataIndex < LineObject->length; u16DataIndex++)
        {
            u8DataTmp = ((SREC_u8HexConverter(u8SrecLine[u8DataOffset]) << 4u)
                        | (SREC_u8HexConverter(u8SrecLine[u8DataOffset + 1u])));
            LineObject->data[u16DataIndex] = u8DataTmp;
            u8DataOffset += 2u;
            u8ChkSum += u8DataTmp;
        }
        /* Get check sum */
        u8ChkSum += ((SREC_u8HexConverter(u8SrecLine[u8DataOffset]) << 4u)
                        | (SREC_u8HexConverter(u8SrecLine[u8DataOffset + 1u])));
        if(u8ChkSum != 0xFFu)
        {
            lineStatus = parseStatus_error;
        }
    }

    return lineStatus;
}


main()
{
    parsedData_struct_t SrecLine;
    parseStatus_t status = parseStatus_idle;
    uint8_t srec[100] = "S903059D5A";
    status = SREC_parseSrecLine(srec, &SrecLine);
    printf("\n**********%d**********\n", status);
    int i =0;
    for(i = 0; i<SrecLine.length ; i++)
    {
        printf("%d ", SrecLine.data[i]);
    }
//    printf("%d", SrecLine);
}
