#include <iostream>
#include <cstdlib>
using namespace std;
template <class T>
void swap1(T &a,T &b) {
	T c; 
	c=a; a=b; b=c;
}
int main(int argc, char* argv[]) {
	int i=20,j=30;
	char c1='A',c2='B';
	float x=20.15, y=35.5;
	//G?i m?u hàm
	swap1(i,j);		
	swap1(c1,c2);
	swap1(x,y);
	cout<<"i="<<i<<" j="<<j<<endl;
	cout<<"c1="<<c1<<" c2="<<c2<<endl;
	cout<<"x="<<x<<" y="<<y<<endl;
	return 0;
}

