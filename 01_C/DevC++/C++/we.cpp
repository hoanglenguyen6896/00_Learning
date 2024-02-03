#include <iostream>
#include <cstdlib>
using namespace std;
class Phanso {
	private:
		int tuso, mauso;
	public:
		Phanso(int ts=0,int ms=1)
		{
			tuso = ts;
			mauso = ms;
		}
		friend Phanso operator*(Phanso a, Phanso b);
  /*  	{ //S? d?ng hàm thành viên
			Phanso q;
			q.tuso = p.tuso* tuso;
			q.mauso = p.mauso * mauso;
			return q;
		}*/
		 //S? d?ng hàm b?n là hàm t? do
		friend Phanso operator+(Phanso p, Phanso q);
		friend ostream& operator<<(ostream & os, Phanso p);
};
Phanso operator*(Phanso a, Phanso b)
{
	Phanso p;
	p.tuso = a.tuso * b.tuso;
	p.mauso = a.mauso * b .mauso;
	return p;
}
Phanso operator+(Phanso p, Phanso q) 
{
	Phanso r;
	r.tuso = p.tuso*q.mauso + p.mauso*q.tuso;
	r.mauso = p.mauso*q.mauso;
	return r;
}

ostream& operator<<(ostream& os, Phanso p){
	os<<p.tuso<<"/"<<p.mauso;
	return os;
}
int main()
{
	Phanso p(2,3),q(4,7);
	cout<<p<<" * "<<q<<" = "<<p*q<<endl;
	cout<<p<<" + "<<q<<" = "<<p+q<<endl;
    
    return system("PAUSE"), EXIT_SUCCESS;
}

