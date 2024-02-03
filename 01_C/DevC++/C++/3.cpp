#include <iostream>
#include <cstdlib>
#include <cmath>
using namespace std;
class Phanso
{
	private:
		int _ts, _ms;
	public:
		int ts,ms;
	void set()
	{
		cout<<"Nhap tu so va mau so:"<<endl;
		cin>>ts>>ms;
		_ts=ts; _ms=ms;
	}
	Phanso operator+(Phanso p1, Phanso p2)
	{
		Phanso p3;
		p3._ts=p1._ts*p2._ms+p1._ms*p2._ts;
		p3._ms=p1._ms*p2._ms;
		return p3;
	}
};
main()
{
	Phanso p1, p2;
	cout<<"Nhap phan so 1\n"; p1.set();
	cout<<"Nhap phan so 2\n"; p2.set();
	Phanso p3;
	p3=p1+p2;
	cout<<"p3="<<p3._ts<<"/"<<p3._ms;
	return 0;
}


