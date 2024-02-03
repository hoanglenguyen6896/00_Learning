#include <iostream>
#include <cstdlib>
#include <math.h>
using namespace std;
class ps{
	private:
		int t, m;
	public:
		ps():t(0), m(1){}
		ps(int a, int b):t(a), m(b){}
		ps operator+(ps a){
			ps r;
			r.t=a.t*this->m+a.m*this->t;
			r.m=a.m*this->m;
			return r;
		}
		ps operator-(ps a){
			ps r;
			r.t=a.m*t-a.t*m;
			r.m=a.m*m;
			return r;
		}
		ps operator*(ps a){
			ps r;
			r.t=t*a.t;
			r.m=m*a.m;
			return r;
		}
		ps operator/(ps a){
			ps r;
			r.t=t*a.m;
			r.m=m*a.t;
			return r;
		}
		friend ostream& operator<<(ostream& os, ps a){
			os << a.t <<"/"<< a.m;
		}
		friend istream& operator>>(istream& is, ps &a){
			is >> a.t >> a.m;
		}
};

main()
{
	ps x;
	ps a(1,2), b(1,4);
	cout<<a<<" / "<<b<<" = "<<a/b<<endl;
	cin>>x; cout<<x;
}
