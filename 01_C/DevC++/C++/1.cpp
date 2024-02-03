#include <iostream>
#include <cstdlib>
#include <math.h>
using namespace std;
main()
{
	double hospitalLatitude[10] = {21.0024661, 21.0152338, 21.0499622, 21.0284025, 21.0035478,
                21.0267909, 21.0259274, 21.0160356, 21.0252491, 21.0004377};
    double hospitalLongitude[10] = {105.8399883, 105.8619055, 105.7897558, 105.8471963, 105.8591086,
                105.807745, 105.8027954, 105.8484891, 105.7883861, 105.8395788};
    double distanceX[10];
    double getLatitude = 20.99655835;
    double getLongitude = 105.8479125;

        for(int i=0; i<10; i++)
        {
            double latitude = hospitalLatitude[i] - getLatitude;
            double longitude = hospitalLongitude[i] - getLongitude;
            distanceX[i] = sqrt(pow(latitude,2) + pow(longitude,2));
            cout << distanceX[i]<<"\n";
        }

}
