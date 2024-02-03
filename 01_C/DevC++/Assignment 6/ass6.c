#ifndef      __A_LL__
#define      __A_LL__

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "ass6.h"
/*******************************************************************************
ass3
|**|10|**|20|**|50|**|**|**|**|**|**|**|**|**|**|**|**|**|**|
nextIndex
|**|*3|**|*5|**|**|**|**|**|**|**|**|**|**|**|**|**|**|**|**|

******************************************************************************/

static uint8_t gs_head = 0xffu;
static uint8_t gs_next = 0xffu;

uint8_t assignment3[20] = {0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,\
                                0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,\
                                0xFF, 0xFF,0xFF, 0xFF};

static uint8_t nextIndex[20] = {0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,\
                                0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,\
                                0xFF, 0xFF,0xFF, 0xFF};
/*******************************************************************************
 * Function name:
 * Function:
 * Return 1 if position is out of [0-19]
 * Return 2 if value is out of [0-100]
 * Return 3 if position has been entered
 * Return 4 if value existed
 ******************************************************************************/
static uint8_t ass6_checkValue(uint8_t iValue, uint8_t iPosition)
{
    uint8_t next = gs_head;
    uint8_t invalid = 0u;
    
    if((iPosition > 19u) && (iPosition < 0u))
    {
        invalid = 1u;
    }
    else if((iValue > 100u) && (iValue < 0u))
    {
        invalid = 2u;
    }
    else
    {
        
        while((next!=0xffu) && (invalid == 0u))
        {
            if (iPosition == next)
            {
                invalid = 3u;
            }
            else if (iValue == assignment3[next])
            {
                invalid = 4u;
            }
            next = nextIndex[next];
        }
    }
    return invalid;
}

/*******************************************************************************
 * Function name:
 * Function:
 ******************************************************************************/
uint8_t ass6_enterElement(void)
{
    uint32_t temp = 0u;
    uint8_t isValid = 0u;
    uint8_t iValue = 0u;
    uint8_t iPosition = 0u;
    uint8_t next = gs_head;
    uint8_t previous = next;
    uint8_t isInsert = 0;
    
    printf("\t1. Enter an element...\n");
    printf("\t   => Enter position: ");
    scanf("%d", &temp);
    iPosition = (uint8_t) temp;
    printf("\t   => Enter value: ");
    scanf("%d", &temp);
    iValue = (uint8_t) temp;
    isValid = ass6_checkValue(iValue, iPosition);
    if(isValid == 0u)
    {
        assignment3[iPosition] = iValue;
        if(gs_head == 0xffu)
        {
            gs_head = iPosition;
            printf("%d***\n", gs_head);
        }
        else
        {
            if(iValue < assignment3[gs_head])
            {
                previous = gs_head;
                gs_head =  iPosition;
                nextIndex[gs_head] = previous;
            }
            else
            {
                while(next != 0xffu && isInsert == 0)
                {
                    if(iValue > assignment3[next])
                    {
                    	previous = next;
                        next = nextIndex[next];
                    }
                    else
                    {
						nextIndex[previous] = iPosition;
						nextIndex[iPosition] = next;
						isInsert == 1;
                    }
                }
            }
        }
    }
}

static void ass6_displayNormal(void)
{
    uint8_t i = 0u;
    for(i = 0u; i < 20u; i++)
    {
        if(assignment3[i] == 0xffu)
        {
            printf("FF ");
        }
        else
        {
            printf("%d ", assignment3[i]);
        }
    }
}

static void ass6_displayNormal1(void)
{
    uint8_t i = 0u;
    for(i = 0u; i < 20u; i++)
    {
        if(nextIndex[i] == 0xffu)
        {
            printf("FF ");
        }
        else
        {
            printf("%d ", nextIndex[i]);
        }
    }
}

static void ass6_displaySortUp(void)
{
    uint8_t next = gs_head;
//    for(next = gs_head; next != 0xffu; next = nextIndex[next])
//    {
//        printf("%d ", assignment3[next]);
//    }
    while(next != 0xffu)
    {
        printf("%d ", assignment3[next]);
        next = nextIndex[next];
    }
}

void ass6_displayArray(void)
{
    uint32_t subOption = 0u;
    printf("\t3. Display array.\n");
    printf("\t   => 1. Display array.\n");
    printf("\t   => 2. Display sort-up array.\n");
    do
    {
        printf("\t   Enter your option: ");
        scanf("%d", &subOption);
    }
    while(subOption<=0 || subOption>=3);
    printf("\t\tYour array is\n");
    printf("\t\t");
    if(subOption == 1)
    {
        ass6_displayNormal();
        printf("\n");
        printf("\t\t");
        ass6_displayNormal1();
    }
    else
    {
        ass6_displaySortUp();
    }
    printf("\n");
}

#endif
