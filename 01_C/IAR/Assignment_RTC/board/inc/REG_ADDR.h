/*******************************************************************************
**     Processors:          MKL46Z128VLL4
**
**     Compilers:           IAR C/C++ Compiler
**
**     Reference manual:    KL46P121M48SF4RM, Rev. 3, July 2013
**     Version:             rev. 1.0, 2020-12-18
**     Abstract:
**          Define macros register address
**     Revisions:
**     - rev. 1.0 (2020-12-18)
**         Initial version.
*******************************************************************************/

#ifndef __REGADDR__
#define __REGADDR__

#define GPIOA_ADDR          (0x400FF000u)   /* Define GPIOA base address */
#define GPIOB_ADDR          (0x400FF040u)   /* Define GPIOB base address */
#define GPIOC_ADDR          (0x400FF080u)   /* Define GPIOC base address */
#define GPIOD_ADDR          (0x400FF0C0u)   /* Define GPIOD base address */
#define GPIOE_ADDR          (0x400FF100u)   /* Define GPIOE base address */

#define PIT_ADDR            (0x40037000u)   /* Define PIT base address */

#define PORTA_ADDR          (0x40049000u)   /* Define PORTA base address */
#define PORTB_ADDR          (0x4004A000u)   /* Define PORTB base address */
#define PORTC_ADDR          (0x4004B000u)   /* Define PORTC base address */
#define PORTD_ADDR          (0x4004C000u)   /* Define PORTD base address */
#define PORTE_ADDR          (0x4004D000u)   /* Define PORTE base address */

#define RTC_ADDR            (0x4003D000u)   /* Define RTC base address */

#define SIM_ADDR            (0x40047000u)   /* Define SIM base address */

#define SYSTICK_ADDR        (0xE000E010u)   /* Define System timer address */

#endif
