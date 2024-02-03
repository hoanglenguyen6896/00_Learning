#include <iostream>
#include <cstdlib>
using namespace std;
class ps
{
	private:
		int x, y;
	public:
		ps()
		{
			x=0; y=1;
		}
		ps operator*(ps a, ps b)
		{
			ps c;
			c.x=a.x*b.x;
			c.y=a.y*b.y;
			return c;
		}
		friend ostream& operator<<(ostream& os, ps a)
		{
			os << a.x <<"\t" << a.y <<endl;
			return os;
		}
}
main()
{
	ps d, s;
	cout <<d*s<<endl;
	system ("pause")
}
