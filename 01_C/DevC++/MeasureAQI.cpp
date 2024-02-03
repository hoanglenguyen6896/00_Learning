// Create by Hoang on Nov. 12th 2019
/*
float 		O3 		0.000
float 		PM2.5 	0.0
short int 	PM10	0
float		CO		0.0
short int	No2		0	
*/
#include "stdio.h"
#include "conio.h"
#include "stdlib.h"
#include "time.h"
#include "AQI_Cal.h"
#include "windows.h"
main()
{
	short int 	i = 0, temp = 0;
	float 		o3_con[24] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	float 		pm25_con[24] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	short int 	pm10_con[24] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	float 		co_con[24] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	short int 	no2_con[24] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	short int 	timestamp = 0, nowCastbreak = 0;
	srand(time(NULL));
	while(nowCastbreak <= 47)
	{
		
		temp = rand() % 5005;
		pm25_con[timestamp] =(float) temp/10;
		printf("[%d] %d\t\t%.1f\n", timestamp, temp, pm25_con[timestamp]);
		printf("AQI = %d\n", getAQI_PM25(pm25_con,nowCastbreak,timestamp));
	/*	srand(time(NULL));
		short int no2_con[timestamp] = rand() % 501;
		printf("NO2_con = %d\n", no2_con[timestamp]);
		printf("AQI_NO2 = %d", getAQI_NO2(no2_con[timestamp]));
		return 0;
		timestamp++;
		if(timestamp == 24) timestamp = 0;*/
		timestamp++;
		nowCastbreak++;
		if(timestamp == 24) timestamp = 0;
		Sleep(1000);
	}
	return 0;
}
