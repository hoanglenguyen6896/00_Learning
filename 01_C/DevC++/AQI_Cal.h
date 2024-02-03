// Create by Hoang on Nov. 12th 2019
#include "AQI_Index.h"
#include "string.h"
#include "math.h"
/*
//Equation
int generalEquation (float ConbreakLow, float ConbreakUp, short int AQILow, short int AQIUp, float concentration);
int generalEquation (short int ConbreakLow, short int ConbreakUp, short int AQILow, short int AQIUp, short int concentration);
//PM2.5 PM10 to NowCast value
float PMtoNowCast(float concentration[24], short int timeStamp);
short int PMtoNowCast25(short int concentration[24], short int timeStamp);
//Get AQI for PM2.5 PM10
short int getAQI_PM25(float concentration[24], short int nowCastorNot, short int timeStamp);
//get NO2 AQI
short int getAQI_NO2 (short int no2_con);
*/
/*--------------------------------------*/
/*--------------------------------------*/
/*----------Function Describle----------*/
/*--------------------------------------*/
/*--------------------------------------*/

//General Equation to Calculate AQI
short int generalEquation (float ConbreakLow, float ConbreakUp, short int AQILow, short int AQIUp, float concentration)
{
	int AQI_I = (AQIUp - AQILow)*(concentration - ConbreakLow)/(ConbreakUp - ConbreakLow) + AQILow;
	return AQI_I;
}
short int generalEquation (short int ConbreakLow, short int ConbreakUp, short int AQILow, short int AQIUp, short int concentration)
{
	int AQI_I = (AQIUp - AQILow)*(concentration - ConbreakLow)/(ConbreakUp - ConbreakLow) + AQILow;
	return AQI_I;
}

//Convert PM2.5 in 1h to PM NowCast
float PMtoNowCast25(float concentration[24], short int timeStamp)
{
	float sub_concentration[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
	float max = 0, min= 0, w= 0, nowCastUp= 0, nowCastDown= 0, nowCast25= 0;
	for(short int i=0; i<=11; i++)
	{
		sub_concentration[i] = concentration[timeStamp];
		timeStamp--;
		if(timeStamp == -1) timeStamp = 23;
		max = sub_concentration[i] > max ? sub_concentration[i]:max;
		min = sub_concentration[i] < min ? sub_concentration[i]:min;
	}
	float sub_w = min/max;
	if(sub_w > 0.5) w = sub_w;
	else w=0.5;
	for (int i=0; i<=11; i++)
	{
		nowCastUp = nowCastUp + pow(w,i)*sub_concentration[i];
		nowCastDown = nowCastDown + pow(w,i);
	}
	nowCast25 = nowCastUp/nowCastDown;
	return nowCast25;
}
//Get AQI for PM2.5
short int getAQI_PM25(float concentration25[24], short int nowCastorNot, short int timeStampX)
{
	float avrPM25 = 0, sumPM25 = 0;
	short int index = 0;
	if (nowCastorNot <= 23) avrPM25 = PMtoNowCast25(concentration25,timeStampX);
	else
	{
		for (int i=0; i<=23; i++)
		{
			sumPM25 += concentration25[i];
		}
		avrPM25 = sumPM25/24;
	}
	if (avrPM25 >= pm25_U[5]) index = 6;
	else
	{
		for (int i=0; i<=5; i++)
		{
			if(pm25_L[i] <= avrPM25 && avrPM25 <= pm25_U[i]) 
			{
				index = i;
				break;
			}
		}
	}
	if (index == 6) return 500;
	else return generalEquation(pm25_L[index], pm25_U[index], aqi_L[index], aqi_U[index], avrPM25);
}

//Conver PM10 in 1h to PM NowCast
short int PMtoNowCast10(short int concentration[24], short int timeStamp)
{
	short int sub_concentration[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
	short int max= 0, min= 0, nowCast10Final= 0;
	float w= 0, nowCastUp= 0, nowCastDown= 0, nowCast10= 0;
	for(short int i=0; i<=11; i++)
	{
		sub_concentration[i] = concentration[timeStamp];
		timeStamp--;
		if(timeStamp == -1) timeStamp = 23;
		max = sub_concentration[i] > max ? sub_concentration[i]:max;
		min = sub_concentration[i] < min ? sub_concentration[i]:min;
	}
	float sub_w = min/max;
	if(sub_w > 0.5) w = sub_w;
	else w=0.5;
	for (int i=0; i<=11; i++)
	{
		nowCastUp = nowCastUp + pow(w,i)*sub_concentration[i];
		nowCastDown = nowCastDown + pow(w,i);
	}
	nowCast10 = nowCastUp/nowCastDown;
	nowCast10Final = round(nowCast10);
	return nowCast10Final;
}
//Get AQI for PM10
short int getAQI_PM10(short int concentration10[24], short int nowCastorNot, short int timeStampX)
{
	float avrPM10 = 0, sumPM10 = 0;
	short int index = 0, avrPM10Final = 0;
	if (nowCastorNot <= 23) avrPM10Final = PMtoNowCast10(concentration10,timeStampX);
	else
	{
		for (int i=0; i<=23; i++)
		{
			sumPM10 += concentration10[i];
		}
		avrPM10 = sumPM10/24;
	}
	avrPM10Final = round(avrPM10);
	if (avrPM10Final >= pm10_U[5]) index = 6;
	else
	{
		for (int i=0; i<=5; i++)
		{
			if(pm10_L[i] <= avrPM10Final && avrPM10Final <= pm25_U[i]) 
			{
				index = i;
				break;
			}
		}
	}
	if (index == 6) return 500;
	else return generalEquation(pm10_L[index], pm10_U[index], aqi_L[index], aqi_U[index], avrPM10Final);
}
//Get AQI for NO2
short int getAQI_NO2 (short int no2_con)
{
	int index = 0;
	if (no2_con > no2_U[5]) index = 6;
	else
	{
		for (int i=0; i<=5; i++)
		{
			if(no2_L[i] <= no2_con && no2_con <= no2_U[i]) 
			{
				index = i;
				break;
			}
		}
	}
	if (index == 6) return 500;
	else return generalEquation(no2_L[index], no2_U[index], aqi_L[index], aqi_U[index], no2_con);
}


