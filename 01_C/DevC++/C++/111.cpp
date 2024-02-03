#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <stdio.h>
using namespace std;
class TS
{
	private:
		int sbd;
		char ht[128];
		float t,l,h;
	public:
		float td()
		{
			return this->t+this->l+this->h;
		}
		void nhapsv()
		{
				cout<<"\t- SBD: "; cin>>sbd;
				cout<<"\t- Ho va ten: "; fflush(stdin); cin.getline(ht,128);
				cout<<"\t- Diem Toan: "; cin>>t; 
				cout<<"\t- Diem Ly: "; cin>>l; 
				cout<<"\t- Diem Hoa: "; cin>>h;
		}
		void hien()
		{
			cout<<setiosflags(ios::left)<<endl<<setiosflags(ios::left)<<setw(20)<<ht<<setiosflags(ios::left)<<setw(10)<<sbd<<setiosflags(ios::left)<<setw(10)<<td();
		}
		friend void swapmax(TS *a,TS *a1,TS d, int n)
		{
			for (int i=0; i<n; i++) a1[i]=a[i];
			for (int i=0; i<n-1; i++)
				for (int j=i+1; j<n; j++)
					if (a1[i].td()>a1[j].td())
					{
						d=a1[i];
						a1[i]=a1[j];
						a1[j]=d;
					}
			for (int i=0; i<n; i++) a1[i].hien();
		}
		friend void max(TS *a, int n)
		{
			TS max;
			cout<<"Sinh vien co tong diem lon nhat la:";
			for (int i=0; i<n; i++)
				if (a[i].td()>=max.td()) max=a[i];
			cout<<endl<<setiosflags(ios::left)<<setw(20)<<"Ho va ten"<<setw(10)<<"SBD"<<setw(10)<<"Tong diem";
			for (int i=0; i<n; i++)
				if(a[i].td()==max.td()) a[i].hien();
		}
		friend void more18(TS *a, int n)
		{
			int m=0;
					
					for(int i=0; i<n; i++)
						if(a[i].td()>18) m++;
					if (m>0) 
					{
						cout<<"Danh sach sinh vien co tong diem tren 18"<<endl<<setiosflags(ios::left)<<setw(20)<<"Ho va ten"<<setw(10)<<"SBD"<<setw(10)<<"Tong diem";
						for(int i=0; i<n; i++)
								if(a[i].td()>18) a[i].hien();
					} else cout<<"Khong co sinh vien co tong diem tren 18"<<endl;
		}
};
main()
{
	TS *a; int n;
	cout<<"Nhap so luong sinh vien: "; cin>>n;
	a=new TS[n+1];
	cout<<endl<<"Nhap danh sach va thong tin sinh vien:"<<endl;
	for(int i=0; i<n; i++)
	{
		cout<<"Thi sinh thu "<<i+1<<":"<<endl;
		a[i].nhapsv();
	}
	char k;
	do
	{
		int d;
		cout<<"Chon 1 yeu cau theo so:\n"<<"\t1. Hien thi danh sach sinh vien vua nhap"<<endl<<"\t2. Sap xep danh sach sinh vien theo thu tu tang dan ve tong diem"<<endl<<"\t3. Sinh vien co tong diem lon nhat"<<endl<<"\t4. Hien thi danh sach sinh vien co tong diem tren 18"<<endl;
		cin>>d;
		switch(d)
		{
			case 1:
					cout<<endl<<setiosflags(ios::left)<<setw(20)<<"Ho va ten"<<setw(10)<<"SBD"<<setw(10)<<"Tong diem";
					for(int i=0; i<n; i++)
						a[i].hien(); break;
			case 2:
					TS *b; TS c;
					b=new TS[n+1];
					cout<<endl<<setiosflags(ios::left)<<setw(20)<<"Ho va ten"<<setw(10)<<"SBD"<<setw(10)<<"Tong diem";
					swapmax(a,b,c,n);
					break;
			case 3:
					max(a,n); break;
			case 4:
					more18(a,n); break;
		}
		cout<<"\n\tTiep tuc chuong trinh (Y/N)?\n"<<"\t";
		cin>>k;
		cout<<endl<<endl;
	}while(k==89 || k==121);
	system("pause");
}
