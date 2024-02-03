// Create by Hoang on Nov. 12th 2019
float 	o3_8L_Good = 0.000, 	o3_8U_Good = 0.054, 
		o3_8L_Mod = 0.055, 		o3_8U_Mod = 0.070,
		o3_8L_UnHeSen = 0.071, 	o3_8U_UnHeSen = 0.085, 
		o3_8L_UnHe = 0.086, 	o3_8U_UnHe = 0.105,
		o3_8L_VeUn = 0.106, 	o3_8U_VeUn = 0.200;
		
float 	o3_1L_UnHeSen = 0.125,	o3_1U_UnHeSen = 0.164,
		o3_1L_UnHe = 0.165,		o3_1U_UnHe = 0.204,
		o3_1L_VeUn = 0.205,		o3_1U_VeUn = 0.404,
		o3_1L_Haza1 = 0.405,	o3_1U_Haza1 = 0.504,
		o3_1L_Haza2 = 0.505,	o3_1U_Haza2 = 0.604;
		
float	pm25_L_Good = 0,		pm25_U_Good = 54,
		pm25_L_Mod = 55,		pm25_U_Mod = 35.4,
		pm25_L_UnHeSen = 35.5,	pm25_U_UnHeSen = 55.4,
		pm25_L_UnHe = 55.5,		pm25_U_UnHe = 150.4,
		pm25_L_VeUn = 150.5,	pm25_U_VeUn = 250.4,
		pm25_L_Haza1 = 250.5,	pm25_U_Haza1 = 350.4,
		pm25_L_Haza2 = 350.5,	pm25_U_Haza2 = 500.4;
		
short int	pm10_L_Good = 0,		pm10_U_Good = 54,
			pm10_L_Mod = 55,		pm10_U_Mod = 154,
			pm10_L_UnHeSen = 155,	pm10_U_UnHeSen = 254,
			pm10_L_UnHe = 255,		pm10_U_UnHe = 354,
			pm10_L_VeUn = 355,		pm10_U_VeUn = 424,
			pm10_L_Haza1 = 425,		pm10_U_Haza1 = 504,
			pm10_L_Haza2 = 505,		pm10_U_Haza2 = 604;
			
/*float	co_L_Good = 0.0,	co_U_Good = 4.4,
		co_L_Mod = 4.5,		co_U_Mod = 9.4,
		co_L_UnHeSen = 9.5,	co_U_UnHeSen = 12.4,
		co_L_UnHe = 12.5,	co_U_UnHe = 15.4,
		co_L_VeUn = 15.5,	co_U_veUn = 30.4,
		co_L_Haza1 = 30.5,	co_U_Haza1 = 40.4,
		co_L_Haza2 = 40.5,	co_U_Haza2 = 50.4;*/
float 	co_L[] = {0.0, 4.5, 9.5, 12.5 15.5, 30.5, 40.5},
		co_U[] = {4.4, 9.4, 12.4, 15.4, 30.4, 40.4, 50.4};
/*short int	no2_L_Good = 0, 		no2_U_Good = 53,
			no2_L_Mod = 54, 		no2_U_Mod = 100,
			no2_L_UnHeSen = 101, 	no2_U_UnHeSen = 360,
			no2_L_UnHe = 361, 		no2_U_UnHe = 649,
			no2_L_VeUn = 650, 		no2_U_VeUn = 1249,
			no2_L_Haza1 = 1250, 	no2_U_Haza1 = 1649,
			no2_L_Haza2 = 1650, 	no2_U_Haza2 = 2049;*/
short int 	no2_L[] = {0, 54, 101, 361, 650, 1250, 1650},
			no2_U[] = {53, 100, 360, 649, 1249, 1659, 2049};	
			
/*short int 	aqi_L_Good = 0,			aqi_U_Good = 50,
			aqi_L_Mod = 51,			aqi_U_Mod = 100,
			aqi_L_UnHeSe = 101,		aqi_U_UnHeSe = 150,
			aqi_L_UnHe = 151,		aqi_U_UnHe = 200,
			aqi_L_VeUn = 201,		aqi_U_VeUn = 300,
			aqi_L_Haza1 = 301,		aqi_U_Haza1 = 400,
			aqi_L_Haza2 = 401,		aqi_U_Haza2 = 500;*/
short int 	aqi_L[] = {0, 51, 101, 151, 201, 301, 401},
			aqi_U[] = {50, 100, 150, 200, 300, 400, 500};
