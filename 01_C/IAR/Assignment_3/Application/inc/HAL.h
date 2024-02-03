#ifndef __HAL__
#define __HAL__

#include "MKL46Z256VLL4.h"

/*******************************************************************************
 * Definitions
*******************************************************************************/
/* Systick count cycle */
#define SYSTICK_COUNT_1MS   20971u

/* Toggle logic output at Pin 29 GPIOE */
#define RED_LED_TOGGLE      GPIOE->PTOR |= (1 << 29)
/* Toggle logic output at Pin 5 GPIOD */
#define GREEN_LED_TOGGLE    GPIOD->PTOR |= (1 << 5)

/* Toggle Cycle for Pin 29 GPIOE (LED Red) */
#define RED_TOGGLE_CYCLE    1000u
/* Toggle Cycle for Pin 5 GPIOC (LED Green) */
#define GREEN_TOGGLE_CYCLE  167u

/*******************************************************************************
 * Prototypes
*******************************************************************************/
/* Config pin */
void HAL_vPinInit(void);
/* Create system timer */
uint8_t HAL_vSysConfig(uint32_t u32Ticks);

#endif /* __HAL__ */
