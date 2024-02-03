#include "AQI.h"
			
AQIFinal::AQIFinal(void)
{
};

short int AQIFinal::AQI_NO2(short int concentration)
{
	short int index=0;
	if(concentration > no2_U[5]) index = 6;
	else
	{
		for(short int i=0; i<=5; i++)
		{
			if(no2_L[i] <= concentration && concentration <= no2_U[i]) 
			{
				index = i;
				break;
			}
		}
		
	}
	if (index == 6) return 500;
	else return generalEquation(no2_L[index], no2_U[index], aqi_L[index], aqi_U[index], concentration);
}
