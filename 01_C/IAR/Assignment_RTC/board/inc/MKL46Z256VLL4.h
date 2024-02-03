/*******************************************************************************
**     Processors:          MKL46Z128VLL4
**
**     Compilers:           IAR C/C++ Compiler
**
**     Reference manual:    KL46P121M48SF4RM, Rev. 3, July 2013
**     Version:             rev. 1.0, 2020-12-18
**     Abstract:
**          CMSIS Peripheral Access Layer for MKL46Z4
**     Revisions:
**     - rev. 1.0 (2020-12-18)
**         Initial version.
**
*******************************************************************************/

#ifndef __MKL46__
#define __MKL46__

#include "REG_ADDR.h"

#define __I                             volatile    /* Read only */
#define __O                             volatile    /* Write only */
#define __IO                            volatile    /* Read/write */

#define int8_t                          char
#define uint8_t                         unsigned char

#define int16_t                         short int
#define uint16_t                        unsigned short int

#define int32_t                         long int
#define uint32_t                        unsigned long int

#define int64_t                         long long int
#define uint64_t                        unsigned long long int

#define LPO_CLK_SOURCE                  1000

/* GPIO - Register Layout Typedef */
typedef struct MKL46_GPIO_STRUCT
{
    __IO    uint32_t PDOR;  /* Port Data Output Register, offset: 0x0 */
    __O     uint32_t PSOR;  /* Port SET Output Register, offset: 0x4 */
    __O     uint32_t PCOR;  /* Port Clear Output Register, offset: 0x8 */
    __O     uint32_t PTOR;  /* Port Toggle Output Register, offset: 0xC */
    __I     uint32_t PDIR;  /* Port Data Input Register, offset: 0x10 */
    __IO    uint32_t PDDR;  /* Port Data Direction Register, offset: 0x14 */
}GPIO_TYPE;

/*Define GPIOA pointer */
#define GPIOA                           ((GPIO_TYPE*) GPIOA_ADDR)
/*Define GPIOB pointer */
#define GPIOB                           ((GPIO_TYPE*) GPIOB_ADDR)
/*Define GPIOC pointer */
#define GPIOC                           ((GPIO_TYPE*) GPIOC_ADDR)
/*Define GPIOD pointer */
#define GPIOD                           ((GPIO_TYPE*) GPIOD_ADDR)
/*Define GPIOE pointer */
#define GPIOE                           ((GPIO_TYPE*) GPIOE_ADDR)

/* PIT - Periodic Interrupt Timer */
typedef struct MKL46_PIT_STRUCT
{
    __IO    uint32_t MCR;
            uint32_t RESERVED_0[55];
    __O     uint32_t LTMR64H;
    __O     uint32_t LTMR64L;
    struct MKL46_TIMER_STRUCT
    {
        __IO    uint32_t LDVAL;
        __O     uint32_t CVAL;
        __IO    uint32_t TCTRL;
        __IO    uint32_t TFLG;
    }TIMER[2];
}PIT_TYPE;

#define PIT                             ((PIT_TYPE*) (PIT_ADDR))

/* PORT - Register Layout Typedef */
typedef struct MKL46_PORT_STRUCT
{
    __IO    uint32_t PCR[32];   /* Pin Control Register n,
                                           array offset: 0x0, array step: 0x4 */
    __O     uint32_t GPCLR;     /* Global Pin Control
                                                   Low Register, offset: 0x80 */
    __O     uint32_t GPCHR;     /* Global Pin Control High Register,
                                                                 offset: 0x84 */
            uint32_t RESERVED[6];
    __IO    uint32_t ISFR;      /* Interrupt Status Flag Register,
                                                                 offset: 0xA0 */
}PORT_TYPE;



/* Configuring the pin for a different pin muxing slot */
#define PIN_MUX_CONTROL_SHIFT           (8u)

/*Define GPIOA pointer */
#define PORTA                           ((PORT_TYPE*) PORTA_ADDR)
/*Define GPIOB pointer */
#define PORTB                           ((PORT_TYPE*) PORTB_ADDR)
/*Define GPIOC pointer */
#define PORTC                           ((PORT_TYPE*) PORTC_ADDR)
/*Define GPIOD pointer */
#define PORTD                           ((PORT_TYPE*) PORTD_ADDR)
/*Define GPIOE pointer */
#define PORTE                           ((PORT_TYPE*) PORTE_ADDR)

/* RTC - Real Time Clock */
typedef struct MKL56_RTC_STRUCT
{
    __IO    uint32_t TSR;   /* RTC Time Seconds Register, offset: 0x00 */
    __IO    uint32_t TPR;   /* RTC Time Prescaler Register, offset: 0x04 */
    __IO    uint32_t TAR;   /* RTC Time Alarm Register, offset: 0x08 */
    __IO    uint32_t TCR;   /* RTC Time Compensation Register, offset: 0x0C */
    __IO    uint32_t CR;    /* RTC Control Register, offset: 0x10 */
    __IO    uint32_t SR;    /* RTC Status Register, offset: 0x14 */
    __IO    uint32_t LR;    /* RTC Lock Register, offset: 0x18 */
    __IO    uint32_t IER;   /* RTC Interrupt Enable Register, offset: 0x1C */
}RTC_TYPE;

#define TPR_MASK                        (0x7FFFu)

#define RTC                             ((RTC_TYPE*) RTC_ADDR)

/* SIM - Register Layout Typedef */
typedef struct MKL46_SIM_STRUCT
{
    __IO    uint32_t SOPT1;     /* System Options Register 1, offset: 0x0 */
    __IO    uint32_t SOPT1CCFG; /* SOPT1 Configuration Register, offset: 0x4 */
            uint32_t RESERVED_0[1023];
    __IO    uint32_t SOPT2;     /* System Options Register 2, offset: 0x1004 */
            uint32_t RESERVED_1;
    __IO    uint32_t SOPT4;     /* System Options Register 4, offset: 0x100C */
    __IO    uint32_t SOPT5;     /* System Options Register 5, offset: 0x1010 */
            uint32_t RESERVED_2;
    __IO    uint32_t SOPT7;     /* System Options Register 7, offset: 0x1018 */
            uint32_t RESERVED_3[2];
    __I     uint32_t SDID;      /* System Device Identification Register,
                                                               offset: 0x1024 */
            uint32_t RESERVED_4[3];
    __IO    uint32_t SCGC4;     /* System Clock Gating Control Register 4,
                                                               offset: 0x1034 */
    __IO    uint32_t SCGC5;     /* System Clock Gating Control Register 5,
                                                               offset: 0x1038 */
    __IO    uint32_t SCGC6;     /* System Clock Gating Control Register 6,
                                                               offset: 0x103C */
    __IO    uint32_t SCGC7;     /* System Clock Gating Control Register 7,
                                                               offset: 0x1040 */
    __IO    uint32_t CLKDIV1;   /* System Clock Divider Register 1,
                                                               offset: 0x1044 */
            uint32_t RESERVED_5;
    __IO    uint32_t FCFG1;     /* Flash Configuration Register 1,
                                                               offset: 0x104C */
    __I     uint32_t FCFG2;     /* Flash Configuration Register 2,
                                                               offset: 0x1050 */
            uint32_t RESERVED_6;
    __I     uint32_t UIDMH;     /* Unique Identification Register Mid-High,
                                                               offset: 0x1058 */
    __I     uint32_t UIDML;     /* Unique Identification Register Mid Low,
                                                               offset: 0x105C */
    __I     uint32_t UIDL;      /* Unique Identification Register Low,
                                                               offset: 0x1060 */
            uint32_t RESERVED_7[39];
    __IO    uint32_t COPC;      /* COP Control Register, offset: 0x1100 */
    __O     uint32_t SRVCOP;    /* Service COP, offset: 0x1104 */
}SIM_TYPE;

/* SOPT1 - System Options Register 1 */
#define SIM_SOPT1_OSC32KSEL_MASK        (0xC0000U)
#define SIM_SOPT1_OSC32KSEL_SHIFT       (18U)
#define SIM_SOPT1_OSC32KSEL(x)          (((uint32_t)(((uint32_t)(x))\
                                                << SIM_SOPT1_OSC32KSEL_SHIFT))\
                                                & SIM_SOPT1_OSC32KSEL_MASK)

/* SCGC5 - System Clock Gating Control Register 5 */
#define SIM_SCGC5_PORTA_SHIFT           (9u)
#define SIM_SCGC5_PORTA_MASK            (0x200u)
#define SIM_SCGC5_PORTA(x)              ((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC5_PORTA_SHIFT)\
                                                & SIM_SCGC5_PORTA_MASK)
#define SIM_SCGC5_PORTB_SHIFT           (10u)
#define SIM_SCGC5_PORTB_MASK            (0x400u)
#define SIM_SCGC5_PORTB(x)              ((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC5_PORTB_SHIFT)\
                                                & SIM_SCGC5_PORTB_MASK)
#define SIM_SCGC5_PORTC_SHIFT           (11u)
#define SIM_SCGC5_PORTC_MASK            (0x800u)
#define SIM_SCGC5_PORTC(x)              ((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC5_PORTC_SHIFT)\
                                                & SIM_SCGC5_PORTC_MASK)
#define SIM_SCGC5_PORTD_SHIFT           (12u)
#define SIM_SCGC5_PORTD_MASK            (0x1000u)
#define SIM_SCGC5_PORTD(x)              ((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC5_PORTD_SHIFT)\
                                                & SIM_SCGC5_PORTD_MASK)
#define SIM_SCGC5_PORTE_SHIFT           (13u)
#define SIM_SCGC5_PORTE_MASK            (0x2000u)
#define SIM_SCGC5_PORTE(x)              ((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC5_PORTE_SHIFT)\
                                                & SIM_SCGC5_PORTE_MASK)

/* SCGC6 - System Clock Gating Control Register 6 */

#define SIM_SCGC6_RTC_SHIFT             (29u)
#define SIM_SCGC6_RTC_MASK              (0x20000000U)
#define SIM_SCGC6_RTC(x)                (((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC6_RTC_SHIFT))\
                                                & SIM_SCGC6_RTC_MASK)

/*Define SIM pointer */
#define SIM                             ((SIM_TYPE*) SIM_ADDR)

/* SYSTICK - Register Layout Typedef */
typedef struct MKL46_SYSTICK_STRUCT
{
    __IO    uint32_t CSR;   /* SysTick Control and Status Register */
    __IO    uint32_t RVR;   /* SysTick Reload Value Register */
    __IO    uint32_t CVR;   /* SysTick Current Value Register */
    __I     uint32_t CALIB; /* SysTick Calibration Value Register */
}SYSTICK_TYPE;

/*  */
#define SYSTICK_MAX_RELOAD_VALUE        (0xFFFFFFu)
/* Systick use processor clock */
#define CLKSRC_SET                      (1u)
#define CLKSRC_SHIFT                    (2u)
#define CLKSRC_ENABLE                   (CLKSRC_SET << CLKSRC_SHIFT)
/* Systick exception status to pending */
#define TICKINT_SET                     (1u)
#define TICKINT_SHIFT                   (1u)
#define TICKINT_ENABLE                  (TICKINT_SET << TICKINT_SHIFT)
/* Enable counter for Systick */
#define SYST_SET                        (1u)
#define SYST_SHIFT                      (0u)
#define SYST_ENABLE                     (SYST_SET << SYST_SHIFT)

/* Define Systick pointer */
#define SYST                            ((SYSTICK_TYPE*) SYSTICK_ADDR)

#endif /* __MKL46__ */
