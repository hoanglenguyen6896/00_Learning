#include <iostream>
#include <cstdlib>
using namespace std;
void dtcv(float &d,float &r,float &dt,float &cv)
{
	dt=d*r;
	cv=d+d+r+r;
}
main()
{
	int n;
	cout<<"Nhap so hinh chu nhat: "; cin >>n;
	float d[100], r[100], dt[100], cv[100];
	for (int i=0; i<n; i++)
	{
		cout <<"Nhap chieu dai va chieu rong HCN thu "<<i+1<<" lan luot la:"<<endl;
		cin >>d[i]>>r[i];
		dtcv(d[i], r[i], dt[i], cv[i]);
	}
	for (int i=0; i<n; i++)
	{
		cout<<"HCN thu "<<i+1<<" co chieu dai la "<<d[i]<<", chieu rong la "<<r[i]<<endl;
		cout<<"\t Co dien tich la "<<dt[i]<<", chu vi la "<<cv[i]<<endl;
	}
	system("PAUSE");
	
}
