#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <stdio.h>
#include <math.h>
using namespace std;
class Point {
	float _x, _y;
	public:
		Point(float x=0, float y=0){  //Hàm t?o v?i tham s? m?c d?nh
			_x=x;
			_y=y;
			cout<<"Goi ham tao"<<endl;
		}
		~Point(){  //Hàm h?y
			cout<<"Goi ham huy"<<endl;
		}
			float distanceTo(Point p){
			float d = (p._x-_x)*(p._x-_x) + (p._y-_y)*(p._y-_y);
			return sqrt(d);
		}

		void setXY(float x, float y);
		float getX(){ return _x; }
		float getY(){ return _y; }
};
int main()
{
	{	Point p1;
		Point p2(10);
		Point p3(20,20);
		cout<<"D12="<<p1.distanceTo(p2)<<endl;
		cout<<"D23="<<p2.distanceTo(p3)<<endl;
	}
	return EXIT_SUCCESS;
}

