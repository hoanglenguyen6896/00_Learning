#include <iostream>   
#include <cstdlib>
using namespace std;
void chuong_trinh_con(void);
class Complex{
	private:
		double re,im;
	public:
		Complex(double r=0, double i=0){re=r; im=i;}
		Complex(const Complex &c): re(c.re),im(c.im) {}
	public:
	    Complex operator + (Complex c);
		Complex operator - (Complex c);
		Complex operator * (Complex c);
		Complex operator / (Complex c);	
	public:
	    friend ostream& operator<<(ostream &out, Complex c)
			{ return(out << '(' << c.re << ","<<c.im<<"i)");}	
};
Complex Complex::operator + (Complex c)
	{return Complex(this->re + c.re, this->im + c.im);} 
Complex Complex::operator - (Complex c)
	{return Complex(this->re - c.re, this->im - c.im);}	
Complex Complex::operator *(Complex c)
	{return Complex((this->re*c.re)-(this->im*c.im),(this->re*c.im)-(c.re*this->im));}
Complex Complex::operator /(Complex c)
{
	Complex d;
	if((c.re!=0.0)&&(c.im!=0.0))
	{
	    d.re=((this->re*c.re)+(this->im*c.im))/((c.re*c.re)+(c.im*c.im));
		d.im=((c.re*this->im)-(this->re*c.im))/((c.re*c.re)+(c.im*c.im));	
	}
	return d;
}		
 
int main(int argc, char** argv) 
{
	chuong_trinh_con();	
	Complex y(1.0,2.3),z(3.4,5.6);
	double a=0.2;
	cout<<y<<"+"<<z<<"+"<<a<<"="<<y+z+a<<endl;
	cout<<y<<"-"<<z<<"="<<y-z<<endl;
	cout<<y<<"*"<<z<<"="<<y*z<<endl;
	cout<<y<<"/"<<z<<"="<<y/z<<endl;
	system("PAUSE");
	return EXIT_SUCCESS;
}
void chuong_trinh_con ()
{system("color f0");}

