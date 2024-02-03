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

#define NULL                            ((void *) 0)

#define true                            (1u)
#define false                           (0u)

/* FTFA - Flash memory module */
typedef struct MKL46_FLASH_STRUCT
{
    __IO    uint8_t FSTAT;  /* Flash Status Register, offset: 0x0 */
    __IO    uint8_t FCNFG;  /* Flash Configuration Register, offset: 0x1 */
    __I     uint8_t FSEC;   /* Flash Security Register, offset: 0x2 */
    __I     uint8_t FOPT;   /* Flash Option Register, offset: 0x3 */
    __IO    uint8_t FCCOB3; /* Flash Common Command Object Registers, offset: 0x4 */
    __IO    uint8_t FCCOB2; /* Flash Common Command Object Registers, offset: 0x5 */
    __IO    uint8_t FCCOB1; /* Flash Common Command Object Registers, offset: 0x6 */
    __IO    uint8_t FCCOB0; /* Flash Common Command Object Registers, offset: 0x7 */
    __IO    uint8_t FCCOB7; /* Flash Common Command Object Registers, offset: 0x8 */
    __IO    uint8_t FCCOB6; /* Flash Common Command Object Registers, offset: 0x9 */
    __IO    uint8_t FCCOB5; /* Flash Common Command Object Registers, offset: 0xA */
    __IO    uint8_t FCCOB4; /* Flash Common Command Object Registers, offset: 0xB */
    __IO    uint8_t FCCOBB; /* Flash Common Command Object Registers, offset: 0xC */
    __IO    uint8_t FCCOBA; /* Flash Common Command Object Registers, offset: 0xD */
    __IO    uint8_t FCCOB9; /* Flash Common Command Object Registers, offset: 0xE */
    __IO    uint8_t FCCOB8; /* Flash Common Command Object Registers, offset: 0xF */
    __IO    uint8_t FPROT3; /* Program Flash Protection Registers, offset: 0x10 */
    __IO    uint8_t FPROT2; /* Program Flash Protection Registers, offset: 0x11 */
    __IO    uint8_t FPROT1; /* Program Flash Protection Registers, offset: 0x12 */
    __IO    uint8_t FPROT0; /* Program Flash Protection Registers, offset: 0x13 */
}FTFA_TYPE;

#define FTFA                            ((FTFA_TYPE*) FTFA_ADDR)

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
    __IO    uint32_t MCR;       /* PIT Module Control Register, offset: 0x0 */
            uint32_t RESERVED_0[55];
    __O     uint32_t LTMR64H;   /* PIT Upper Lifetime Timer Register,
                                                                 offset: 0xE0 */
    __O     uint32_t LTMR64L;   /* PIT Lower Lifetime Timer Register,
                                                                 offset: 0xE4 */
    struct MKL46_TIMER_STRUCT   /* offset: 0x100, array step: 0x10 */
    {
        __IO    uint32_t LDVAL; /* Timer Load Value Register,
                                        array offset: 0x100, array step: 0x10 */
        __O     uint32_t CVAL;  /* Current Timer Value Register,
                                        array offset: 0x104, array step: 0x10 */
        __IO    uint32_t TCTRL; /* Timer Control Register,
                                        array offset: 0x108, array step: 0x10 */
        __IO    uint32_t TFLG;  /* Timer Flag Register,
                                        array offset: 0x10C, array step: 0x10 */
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

/* PCR -  Pin Control Register */
#define PORT_PCR_MUX_SHIFT              (8U)
#define PORT_PCR_MUX_MASK               (0x700U)
#define PORT_PCR_MUX(x)                 (((uint32_t)(((uint32_t)(x))\
                                                << PORT_PCR_MUX_SHIFT))\
                                                & PORT_PCR_MUX_MASK)

/*Define PORTA pointer */
#define PORTA                           ((PORT_TYPE*) PORTA_ADDR)
/*Define PORTB pointer */
#define PORTB                           ((PORT_TYPE*) PORTB_ADDR)
/*Define PORTC pointer */
#define PORTC                           ((PORT_TYPE*) PORTC_ADDR)
/*Define PORTD pointer */
#define PORTD                           ((PORT_TYPE*) PORTD_ADDR)
/*Define PORTE pointer */
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

/* TPR - Time Prescaler Register */
#define RTC_TPR_MASK                    (0x7FFFu)
/* CR - Control Register */
#define RTC_CR_SWR_SHIFT                (0u)
#define RTC_CR_SWR_MASK                 (1u)
#define RTC_CR_SWR(x)                   ((uint32_t)(((uint32_t)(x))\
                                                << RTC_CR_SWR_SHIFT)\
                                                & RTC_CR_SWR_MASK)
/* SR - Status Register */
#define RTC_SR_TCE_SHIFT                (4U)
#define RTC_SR_TCE_MASK                 (0x10U)
#define RTC_SR_TCE(x)                   (((uint32_t)(((uint32_t)(x))\
                                                << RTC_SR_TCE_SHIFT))\
                                                & RTC_SR_TCE_MASK)

/* Define RTC pointer */
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
#define SIM_SOPT1_OSC32KSEL_SHIFT       (18U)
#define SIM_SOPT1_OSC32KSEL_MASK        (0xC0000U)
#define SIM_SOPT1_OSC32KSEL(x)          (((uint32_t)(((uint32_t)(x))\
                                                << SIM_SOPT1_OSC32KSEL_SHIFT))\
                                                & SIM_SOPT1_OSC32KSEL_MASK)
/* SOPT2 - System Options Register 2 */
#define SIM_SOPT2_UART0SRC_SHIFT        (26U)
#define SIM_SOPT2_UART0SRC_MASK         (0xC000000U)
#define SIM_SOPT2_UART0SRC(x)           (((uint32_t)(((uint32_t)(x))\
                                                << SIM_SOPT2_UART0SRC_SHIFT))\
                                                & SIM_SOPT2_UART0SRC_MASK)
#define SIM_SOPT2_PLLFLLSEL_SHIFT       (16u)
#define SIM_SOPT2_PLLFLLSEL_MASK        (0x10000u)
#define SIM_SOPT2_PLLFLLSEL(x)          (((uint32_t) (((uint32_t)(x))\
                                                << SIM_SOPT2_PLLFLLSEL_SHIFT))\
                                                & SIM_SOPT2_PLLFLLSEL_MASK)
/* SCGC4 - System Clock Gating Control Register 4 */
#define SIM_SCGC4_UART0_SHIFT           (10u)
#define SIM_SCGC4_UART0_MASK            (0x400u)
#define SIM_SCGC4_UART0(x)              ((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC4_UART0_SHIFT)\
                                                & SIM_SCGC4_UART0_MASK)

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
#define SIM_SCGC6_RTC_MASK              (0x20000000u)
#define SIM_SCGC6_RTC(x)                (((uint32_t)(((uint32_t)(x))\
                                                << SIM_SCGC6_RTC_SHIFT))\
                                                & SIM_SCGC6_RTC_MASK)
/* CLKDIV1 -  System Clock Divider Register 1 */
#define SIM_CLKDIV1_OUTDIV1_SHIFT        (28u)
#define SIM_CLKDIV1_OUTDIV1_MASK         (0xF0000000u)
#define SIM_CLKDIV1_OUTDIV1(x)           (((uint32_t)(((uint32_t)(x))\
                                                << SIM_CLKDIV1_OUTDIV1_SHIFT))\
                                                & SIM_CLKDIV1_OUTDIV1_MASK)
#define SIM_CLKDIV1_OUTDIV4_SHIFT        (16u)
#define SIM_CLKDIV1_OUTDIV4_MASK         (0x70000u)
#define SIM_CLKDIV1_OUTDIV4(x)           (((uint32_t)(((uint32_t)(x))\
                                                << SIM_CLKDIV1_OUTDIV4_SHIFT))\
                                                & SIM_CLKDIV1_OUTDIV4_MASK)
/*Define SIM pointer */
#define SIM                             ((SIM_TYPE*) SIM_ADDR)

typedef struct {
    __IO    uint8_t BDH; /* UART Baud Rate Register High, offset: 0x0 */
    __IO    uint8_t BDL; /* UART Baud Rate Register Low, offset: 0x1 */
    __IO    uint8_t C1;  /* UART Control Register 1, offset: 0x2 */
    __IO    uint8_t C2;  /* UART Control Register 2, offset: 0x3 */
    __IO    uint8_t S1;  /* UART Status Register 1, offset: 0x4 */
    __IO    uint8_t S2;  /* UART Status Register 2, offset: 0x5 */
    __IO    uint8_t C3;  /* UART Control Register 3, offset: 0x6 */
    __IO    uint8_t D;   /* UART Data Register, offset: 0x7 */
    __IO    uint8_t MA1; /* UART Match Address Registers 1, offset: 0x8 */
    __IO    uint8_t MA2; /* UART Match Address Registers 2, offset: 0x9 */
    __IO    uint8_t C4;  /* UART Control Register 4, offset: 0xA */
    __IO    uint8_t C5;  /* UART Control Register 5, offset: 0xB */
}UART0_TYPE;

/* BDH - UART Baud Rate Register High */
#define UART0_BDH_SBNS_SHIFT            (5u)
#define UART0_BDH_SBNS_MASK             (0x20u)
#define UART0_BDH_SBNS(x)               (((uint8_t)(((uint8_t)(x))\
                                                << UART0_BDH_SBNS_SHIFT))\
                                                & UART0_BDH_SBNS_MASK)
#define UART0_BDH_SBR_SHIFT             (0u)
#define UART0_BDH_SBR_MASK              (0x1Fu)
#define UART0_BDH_SBR(x)                (((uint8_t)(((uint8_t)(x))\
                                                << UART0_BDH_SBR_SHIFT))\
                                                & UART0_BDH_SBR_MASK)
/* BDL - UART Baud Rate Register Low */
#define UART0_BDL_SBR_SHIFT              (0u)
#define UART0_BDL_SBR_MASK               (0xFFu)
#define UART0_BDL_SBR(x)                 (((uint8_t)(((uint8_t)(x))\
                                                << UART0_BDL_SBR_SHIFT))\
                                                & UART0_BDL_SBR_MASK)
/* C1 - UART Control Register 1 */

#define UART0_C1_M_SHIFT                (4u)
#define UART0_C1_M_MASK                 (0x10u)
#define UART0_C1_M(x)                   (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C1_M_SHIFT))\
                                                & UART0_C1_M_MASK)
#define UART0_C1_PE_SHIFT               (1u)
#define UART0_C1_PE_MASK                (0x2u)
#define UART0_C1_PE(x)                  (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C1_PE_SHIFT))\
                                                & UART0_C1_PE_MASK)
#define UART0_C1_PT_SHIFT               (0u)
#define UART0_C1_PT_MASK                (0x1u)
#define UART0_C1_PT(x)                  (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C1_PT_SHIFT))\
                                                & UART0_C1_PT_MASK)
/* C2 - UART Control Register 2 */
#define UART0_C2_RIE_SHIFT              (5u)
#define UART0_C2_RIE_MASK               (0x20u)
#define UART0_C2_RIE(x)                 (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C2_RIE_SHIFT))\
                                                & UART0_C2_RIE_MASK)
#define UART0_C2_TE_SHIFT               (3u)
#define UART0_C2_TE_MASK                (0x8u)
#define UART0_C2_TE(x)                  (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C2_TE_SHIFT))\
                                                & UART0_C2_TE_MASK)
#define UART0_C2_RE_SHIFT               (2u)
#define UART0_C2_RE_MASK                (0x4u)
#define UART0_C2_RE(x)                  (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C2_RE_SHIFT))\
                                                & UART0_C2_RE_MASK)
/* S1 - UART Status Register 1  */
#define UART0_S1_TC_SHIFT               (6u)
#define UART0_S1_TC_MASK                (0x40u)
#define UART0_S1_TC(x)                  (((uint8_t)(((uint8_t)(x))\
                                                << UART0_S2_TC_SHIFT))\
                                                & UART0_S2_TC_MASK)
#define UART0_S1_RDRF_SHIFT             (5u)
#define UART0_S1_RDRF_MASK              (0x20u)
#define UART0_S1_RDRF(x)                (((uint8_t)(((uint8_t)(x))\
                                                << UART0_S2_RDRF_SHIFT))\
                                                & UART0_S2_RDRF_MASK)
/* S2 - UART Status Register 2  */
#define UART0_S2_MSBF_SHIFT             (5u)
#define UART0_S2_MSBF_MASK              (0x20u)
#define UART0_S2_MSBF(x)                (((uint8_t)(((uint8_t)(x))\
                                                << UART0_S2_MSBF_SHIFT))\
                                                & UART0_S2_MSBF_MASK)
#define UART0_S2_RXINV_SHIFT            (4u)
#define UART0_S2_RXINV_MASK             (0x10u)
#define UART0_S2_RXINV(x)               (((uint8_t)(((uint8_t)(x))\
                                                << UART0_S2_RXINV_SHIFT))\
                                                & UART0_S2_RXINV_MASK)
/* C3 - UART Control Register 3 */
#define UART0_C3_TXINV_SHIFT            (4u)
#define UART0_C3_TXINV_MASK             (0x10u)
#define UART0_C3_TXINV(x)               (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C3_TXINV_SHIFT))\
                                                & UART0_C3_TXINV_MASK)
/* C4 - UART Control Register 4 */
#define UART0_C4_M10_SHIFT              (5u)
#define UART0_C4_M10_MASK               (0x2u)
#define UART0_C4_M10(x)                 (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C4_M10_SHIFT))\
                                                & UART0_C4_M10_MASK)
#define UART0_C4_OSR_SHIFT              (0u)
#define UART0_C4_OSR_MASK               (0x1Fu)
#define UART0_C4_OSR(x)                 (((uint8_t)(((uint8_t)(x))\
                                                << UART0_C4_OSR_SHIFT))\
                                                & UART0_C4_OSR_MASK)
/* Define UART0 pointer */
#define UART0                           ((UART0_TYPE*) UART0_ADDR)

/*******************************************************************************
* Core
*******************************************************************************/
/* SYSTICK - Register Layout Typedef */
typedef struct
{
    __IO    uint32_t ISER;          /* Interrupt Set Enable Register */
            uint32_t RESERVED0[31U];
    __IO    uint32_t ICER;          /* Interrupt Clear Enable Register */
            uint32_t RSERVED1[31U];
    __IO    uint32_t ISPR;          /* Interrupt Set Pending Register */
            uint32_t RESERVED2[31U];
    __IO    uint32_t ICPR;          /* Interrupt Clear Pending Register */
            uint32_t RESERVED3[31U];
            uint32_t RESERVED4[64U];
    __IO    uint32_t IPR[8U];       /* Interrupt Priority Register */
}NVIC_TYPE;

typedef struct
{
    __I     uint32_t CPUID;         /* CPUID Base Register */
    __IO    uint32_t ICSR;          /* Interrupt Control and State Register */
    __IO    uint32_t VTOR;          /* Vector Table Offset Register */
            uint32_t RESERVED0;
    __IO    uint32_t AIRCR;         /* Application Interrupt and Reset Control Register */
    __IO    uint32_t SCR;           /* System Control Register */
    __I     uint32_t CCR;           /* Configuration Control Register */
            uint32_t RESERVED1;
    __IO    uint32_t SHP[2U];       /* System Handlers Priority Registers. [0] is RESERVED */
    __IO    uint32_t SHCSR;         /* System Handler Control and State Register */
} SCB_Type;

#define SCB                 ((SCB_Type*) SCB_BASE)

/* Define Nested Vectored Interrupt Controller pointer */
#define NVIC                            ((NVIC_TYPE*) NVIC_ADDR)

/* SYSTICK - Register Layout Typedef */
typedef struct MKL46_SYSTICK_STRUCT
{
    __IO    uint32_t CSR;   /* SysTick Control and Status Register */
    __IO    uint32_t RVR;   /* SysTick Reload Value Register */
    __IO    uint32_t CVR;   /* SysTick Current Value Register */
    __I     uint32_t CALIB; /* SysTick Calibration Value Register */
}SYSTICK_TYPE;

/* RVR - Reload value register */
#define SYST_RVR_MAX_VALUE              (0xFFFFFFu)
/* CSR - SysTick Control and Status Register */
#define SYST_CSR_CLK_SHIFT              (2u)
#define SYST_CSR_CLK_MASK               (0x4u)
#define SYST_CSR_CLK(x)                 (((uint32_t)(((uint32_t)(x))\
                                                << SYST_CSR_CLK_SHIFT))\
                                                & SYST_CSR_CLK_MASK)
#define SYST_CSR_TICKINT_SHIFT          (1u)
#define SYST_CSR_TICKINT_MASK           (0x2u)
#define SYST_CSR_TICKINT(x)             (((uint32_t)(((uint32_t)(x))\
                                                << SYST_CSR_TICKINT_SHIFT))\
                                                & SYST_CSR_CLK_MASK)
#define SYST_CSR_ENABLE_SHIFT           (0u)
#define SYST_CSR_ENABLE_MASK            (0x1u)
#define SYST_CSR_ENABLE(x)              (((uint32_t)(((uint32_t)(x))\
                                                << SYST_CSR_CLK_SHIFT))\
                                                & SYST_CSR_CLK_MASK)
/* Define Systick pointer */
#define SYST                            ((SYSTICK_TYPE*) SYSTICK_ADDR)

/*******************************************************************************
 * Function name: NVIC_EnableIRQ
 * Description: Disable a device-specific interrupt in the NVIC.
*******************************************************************************/
static inline void NVIC_DisableIRQ(uint32_t IRQn)
{
  NVIC->ICER = (uint32_t)(1u << (((uint32_t)(int32_t)IRQn) & 0x1Fu));
}

/*******************************************************************************
 * Function name: NVIC_EnableIRQ
 * Description: Enables a device-specific interrupt in the NVIC.
*******************************************************************************/
static inline void NVIC_EnableIRQ(uint32_t IRQn)
{
  NVIC->ISER = (uint32_t)(1u << (((uint32_t)(int32_t)IRQn) & 0x1Fu));
}


#endif /* __MKL46__ */
