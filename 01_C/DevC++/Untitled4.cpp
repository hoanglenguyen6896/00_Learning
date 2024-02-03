// Create by Hoang on Nov. 12th 2019
#include "AQI_Index.h"
#include "string.h"

string type[] = {"O3 in 8", "O3 in 1", "PM2.5 normal", "PM2.5 NowCast"
					"PM10 normal", "PM10 NowCast",
					"CO", "NO2"};
//
int generalEquation (float ConbreakLow, float ConbreakUp, short int ILow, short int IUp, float concentration)
{
	int AQI_I = (IUp - ILow)*(concentration - ConbreakLow)/(ConbreakUp - ConbreakLow) + ILow;
	return AQI_I;
}

int getAQI_NO2 (int concentration, short int index)
{
	
}

int getAQI_O3(float concentration, short int index)
{
	
}
float getO3NowCast(float o3_concentration)
{
	
}

