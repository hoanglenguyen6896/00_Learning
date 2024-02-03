#include "SREC.h"

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Convert char to number */
static uint8_t SREC_hexConverter(uint8_t character);

/*******************************************************************************
* Code
*******************************************************************************/

/*******************************************************************************
 * Function name: SREC_hexConverter
 * Description: Convert char to number
*******************************************************************************/
static uint8_t SREC_hexConverter(uint8_t character)
{
    uint8_t hexValue = 0xFFu;
    if((character >= '0') && (character <= '9'))
    {
        hexValue = character - '0';
    }
    else if((character >= 'A') && (character <= 'F'))
    {
        hexValue = character - 'A' + 10u;
    }

    return hexValue;
}

/*******************************************************************************
 * Function name: SREC_parsesrecLine
 * Description: Parse a Srec line
*******************************************************************************/
parseStatus_t SREC_parsesrecLine(uint8_t *srecLine,
                                            parsedData_struct_t *LineObject)
{
    /* Line return status after parse */
    parseStatus_t lineStatus = parseStatus_error;
    uint8_t srecType; /* Srecord type */
    uint8_t byteCount; /* Byte count of a Srec line */
    uint32_t addr = 0u; /* Address of a Srec line */
    uint8_t numberOfAddrByte; /* Number of Address byte in a Srec line */
    uint8_t dataTmp;
    uint16_t dataIndex;
    uint8_t dataOffset = 4u; /* Data offset (Stype + ByteCount) */
    uint8_t chkSum = 0u; /* Checksum */

    /* Check Char[0] and get Srecord type */
    if(srecLine[0u] == 'S')
    {
        srecType = SREC_hexConverter(srecLine[1u]);
        switch(srecType)
        {
            case 0u:
                lineStatus = parseStatus_start;
                break;
            case 1u:
            case 2u:
            case 3u:
                lineStatus = parseStatus_inProgress;
                numberOfAddrByte = srecType + 1u;
                break;
            case 4u:
                lineStatus = parseStatus_error;
                break;
            case 5u:
            case 6u:
                /* Optional, in MOCK, I skip check line count */
                lineStatus = parseStatus_optional;
                numberOfAddrByte = srecType - 3u;
                break;
            case 7u:
            case 8u:
            case 9u:
                lineStatus = parseStatus_end;
                numberOfAddrByte = 11u - srecType;
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
        byteCount = (uint8_t) ((SREC_hexConverter(srecLine[2u]) << 4u)
                        | (SREC_hexConverter(srecLine[3u])));
        chkSum += byteCount;
        /* Get data */
        for(dataIndex = 0u; dataIndex < numberOfAddrByte; dataIndex++)
        {
            dataTmp = (uint8_t) ((SREC_hexConverter(srecLine[dataOffset]) << 4u)
                        | (SREC_hexConverter(srecLine[dataOffset + 1u])));
            addr = (addr << 8u) | dataTmp;
            chkSum += dataTmp;
            dataOffset += 2u;
        }
        LineObject->address = addr;
        /* Get Data length */
        /* 1 byte chksum */
        LineObject->length = byteCount - numberOfAddrByte - 1u;
        for(dataIndex = 0u; dataIndex < LineObject->length; dataIndex++)
        {
            dataTmp = (uint8_t) ((SREC_hexConverter(srecLine[dataOffset]) << 4u)
                        | (SREC_hexConverter(srecLine[dataOffset + 1u])));
            LineObject->data[dataIndex] = dataTmp;
            dataOffset += 2u;
            chkSum += dataTmp;
        }
        /* Get and check check sum */
        chkSum += (uint8_t) ((SREC_hexConverter(srecLine[dataOffset]) << 4u)
                        | (SREC_hexConverter(srecLine[dataOffset + 1u])));
        if(chkSum != 0xFFu)
        {
            lineStatus = parseStatus_error;
        }
    }

    return lineStatus;
}
