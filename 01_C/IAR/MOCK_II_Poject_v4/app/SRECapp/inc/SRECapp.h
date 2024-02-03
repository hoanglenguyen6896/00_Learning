#ifndef __SRECAPP__
#define __SRECAPP__

#include "MKL46Z4.h"
#include "QUEUE.h"

/*******************************************************************************
 * Prototypes
*******************************************************************************/

/* Point to a free row of queue to put */
void SRECapp_init(void);
/* Callback function to put character into queue */
void SRECapp_callback(uint8_t character);

#endif  /* __SRECAPP__ */
