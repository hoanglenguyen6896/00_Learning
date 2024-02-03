#include <iostream>
#include <cstdlib>
using namespace std;
class Phanso {
	int tuso, mauso;
	public:
		Phanso(int ts=0,int ms=1){
			tuso = ts;
			mauso = ms;
		}
		Phanso operator*(Phanso p);
		 //S? d?ng hàm b?n là hàm t? do
		/*friend*/ Phanso operator+(Phanso p)//;
		{
			Phanso r;
			r.tuso=p.tuso*this->mauso + p.mauso*this->tuso;
			r.mauso=p.mauso*this->mauso;
			return r;
		}
		friend ostream& operator<<(ostream & os, Phanso p);
};
/*Phanso operator+(Phanso p, Phanso q) {
	Phanso r;
	r.tuso = p.tuso*q.mauso + p.mauso*q.tuso;
	r.mauso = p.mauso*q.mauso;
	return r;
}*/
Phanso Phanso::operator*(Phanso p)
		{
			Phanso q;
			q.tuso = p.tuso* this->tuso;
			q.mauso = p.mauso * this->mauso;
			return q;
		}
ostream& operator<<(ostream & os, Phanso p){
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


