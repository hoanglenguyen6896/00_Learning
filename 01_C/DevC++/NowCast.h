#include "math.h"
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
