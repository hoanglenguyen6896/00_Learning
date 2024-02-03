#include "math.h"
class AQIFinal
{
	public:
		AQIFinal(void);
		short int AQI_O3();
		short int AQI_PM25();
		short int AQI_PM10();
		short int AQI_CO();							//
		short int AQI_NO2(short int concentration); //
	//private:
		short int 	aqi_L[7] = {0, 51, 101, 151, 201, 301, 401},
					aqi_U[7] = {50, 100, 150, 200, 300, 400, 500};
	short int generalEquation (float ConbreakLow, float ConbreakUp, short int AQILow, short int AQIUp, float concentration)
	{
		float AQI_1 = (AQIUp - AQILow)*(concentration - ConbreakLow)/(ConbreakUp - ConbreakLow) + AQILow;
		short int AQI_I = round(AQI_1);
		return AQI_I;
	}
	short int generalEquation (short int ConbreakLow, short int ConbreakUp, short int AQILow, short int AQIUp, short int concentration)
	{
		float AQI_1 = (AQIUp - AQILow)*(concentration - ConbreakLow)/(ConbreakUp - ConbreakLow) + AQILow;
		short int AQI_I = round(AQI_1);
		return AQI_I;
	}
};
