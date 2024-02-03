#ifndef      __A_LL__
#define      __A_LL__

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "ass6.h"


void menu(void)
{
    static uint8_t option = 0u;
    static uint8_t value = 0u;
    static uint8_t position = 0u;
    uint32_t exitFlag = 0u;
    printf("********************************************************\n");
    printf("*************Array management by linked list************\n");
    printf("********************************************************\n");
    printf("**** 1. Enter an element.                           ****\n");
    printf("**** 2. Delete an element.                          ****\n");
    printf("**** 3. Display array.                              ****\n");
    printf("**** 4. Exit.                                       ****\n");
    printf("********************************************************\n");
    printf("********************************************************\n");
    while(exitFlag != 4)
    {
        printf("Enter your option: \n");
        scanf("%d", &exitFlag);
        switch(exitFlag)
        {
            case(1):
                printf("1\n");
                ass6_enterElement();
                break;
            case(2):
                printf("2\n");
                break;
            case(3):
                printf("3\n");
                ass6_displayArray();
                break;
            case(4):
                printf("4\n");
                break;
        }
    }
}

#endif


