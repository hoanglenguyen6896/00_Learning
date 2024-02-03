#include <iostream>
#include <cstdlib>
using namespace std;

int main() 
{
    char h[256];
    cout <<"Nhap chuoi khong qua 200 ki tu:"<<endl;
    cin.get(h,200);
    int i, k=0;
    for(i=0;i<=200;i++)
    {
    	if (int (h[i])==32) k++;
    }
    cout<<"So tu cua chuoi la: "<<k+1<<endl;
    system("pause");
    return 0;
}

