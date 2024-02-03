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
 * Function name: ass6_printError
 * Function: Display error
 ******************************************************************************/
static void ass6_printError(uint8_t isValid)
{
	switch(isValid)
	{
		case(1):
			printf("\t   => Error: Position is out of [0-19]\n");
			break;
		case(2):
			printf("\t   => Error: Value is out of [0-100]\n");
			break;
		case(3):
			printf("\t   => Error: Position has been entered\n");
			break;
		case(4):
			printf("\t   => Error: Value has already existed\n");
			break;
	}
}
/*******************************************************************************
 * Function name: ass6_checkValue
 * Function:
 * Return 1 if position is out of [0-19]
 * Return 2 if value is out of [0-100]
 * Return 3 if position has been entered
 * Return 4 if value existed
 ******************************************************************************/
static uint8_t ass6_checkPosition(uint8_t iPosition)
{
	uint8_t next = gs_head;
    uint8_t invalid = 0u;
    if((iPosition > 19u) || (iPosition < 0u))
    {
        invalid = 1u;
    }
    else
    {
    	while((next != 0xffu) && (invalid == 0u))
        {
            if (iPosition == next)
            {
                invalid = 3u;
            }
            next = nextIndex[next];
        }
	}
	
	return invalid;
}

static uint8_t ass6_checkValue(uint8_t iValue, uint8_t *iValPos,\
														uint8_t *iValPrePos)
{
    uint8_t next = gs_head;
    uint8_t invalid = 0u;
    
	*iValPos = next;
	*iValPrePos = *iValPos;
	
    if((iValue > 100u) || (iValue < 0u))
    {
        invalid = 2u;
    }
    else
    {
        while((next != 0xffu) && (invalid == 0u))
        {
			if (iValue == assignment3[next])
            {
                invalid = 4u;
                *iValPos = next;
            }
            else
			{
				*iValPrePos = next;
				next = nextIndex[next];
			}
        }
    }
    
    return invalid;
}

/*******************************************************************************
 * Function name:
 * Function:
 ******************************************************************************/
void ass6_enterElement(void)
{
    uint32_t temp = 0u;
    uint8_t isInsert = 0u;
    
    uint8_t next = gs_head;
    uint8_t previous = next;
    
    uint8_t valuePos = 0u;
    uint8_t valuePrePos = 0u;
    uint8_t iValue = 0u;
    uint8_t iPosition = 0u;
	uint8_t isValidValue = 0u;
    uint8_t isValidPosition = 0u;
    
    printf("\t1. Enter an element...\n");
    printf("\t   => Enter position: ");
    scanf("%d", &temp);
    iPosition = (uint8_t) temp;
    isValidPosition = ass6_checkPosition(iPosition);

    printf("\t   => Enter value: ");
    scanf("%d", &temp);
    iValue = (uint8_t) temp;
    isValidValue = ass6_checkValue(iValue, &valuePos, &valuePrePos);

    if((isValidValue == 0u) && (isValidPosition == 0))
    {
        assignment3[iPosition] = iValue;
        if(gs_head == 0xffu)
        {
            gs_head = iPosition;
            next = gs_head;
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
						if(next == 0xffu)
						{
							assignment3[iPosition] = iValue;
							nextIndex[previous] = iPosition;
						}
                    }
                    else
                    {
						nextIndex[previous] = iPosition;
						nextIndex[iPosition] = next;
						isInsert = 1;
                    }
                }
            }
        }
        printf("\t   => Enter Successfully!!!!\n");
    }
    else
    {
		if(isValidPosition != 0)
		{
			ass6_printError(isValidPosition);
		}
		if(isValidValue != 0)
		{
			ass6_printError(isValidValue);
		}
	}
}

void ass6_deleteElements(void)
{
	uint32_t temp = 0u;
    
    uint8_t next = gs_head;
    uint8_t previous = next;
    
    uint8_t iValue = 0u;
    uint8_t valuePos = 0u;
    uint8_t valuePrePos = 0u;
    uint8_t isValidValue = 0u;
    
    uint8_t isDelete = 0u;
	
	printf("\t2. Delete an element...\n");
	printf("\t   => Enter value: ");
    scanf("%d", &temp);
    iValue = (uint8_t) temp;
    isValidValue = ass6_checkValue(iValue, &valuePos, &valuePrePos);
    if(isValidValue == 4u)
    {
    	assignment3[valuePos] = 0xffu;
    	if(valuePos == gs_head)
    	{
			//delHead
			gs_head = nextIndex[valuePos];
			nextIndex[valuePos] = 0xffu;
		}
		else if(nextIndex[valuePos] == 0xffu)
		{
			//deltail
			nextIndex[valuePrePos] = 0xffu;
		}
		else
		{
			//delAt
			nextIndex[valuePrePos] = nextIndex[valuePos];
			nextIndex[valuePos] = 0xffu;
		}
		printf("\t   => Delete Successfully!!!!\n");
 	}
	else
	{
		printf("\t   => Error: Value does not exist in array.\n");
	}
}

static void ass6_displayNormal(void)
{
    uint8_t i = 0u;
    for(i = 0u; i < 20u; i++)
    {
        if(assignment3[i] == 0xffu)
        {
            printf("%-4s", "FF");
        }
        else
        {
            printf("%-4d", assignment3[i]);
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
            printf("%-4s", "FF");
        }
        else
        {
            printf("%-4d", nextIndex[i]);
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
    
    if(subOption == 1)
    {
    	printf("\t\tYour array is\n");
    	printf("\t\t* assignment3[]\n\t\t");
        ass6_displayNormal();
        printf("\n");
        printf("\t\t* nextIndex\n\t\t");
        ass6_displayNormal1();
    }
    else
    {
    	printf("\t\tYour array is after sorted\n");
    	printf("\t\t* assignment3[]\n\t\t");
        ass6_displaySortUp();
    }
    printf("\n");
}

