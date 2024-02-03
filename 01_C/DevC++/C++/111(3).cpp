/*
Xay dung lop Sinh Vien gom cac ycau:
	- MaSV, TenSV, NamSinh, DiemTB
	- Ham tao ham huy de khoi tao lop
	- Ham Nhap() dung de nhap slieu sv
	- Ham HienThi() de hien thi thong tin sinh vien
*/
#include <iostream>
#include <cstdlib>
#include <stdio.h>

using namespace std;
class SinhVien{
	private:
		int MaSV, NamSinh;
		char TenSV[100];
		float DiemTB;
	public:
		SinhVien()
		{
			MaSV=0; TenSV[100]='a'; NamSinh=1990; DiemTB=10.0;
		}
		~SinhVien(){}
		void Nhap()
		{
				cout<<"Ma SV: "; cin>>MaSV;
				cout<<"Ten SV: "; fflush(stdin); cin.getline(TenSV,100);
				cout<<"Nam Sinh: "; cin>>NamSinh;
				cout<<"Diem TB: "; cin>>DiemTB;
		}
		void HienThi()
		{
				cout<<"Ma SV: "<<MaSV<<endl;
				cout<<"Ten SV: "<<TenSV<<endl;
				cout<<"Nam Sinh: "<<NamSinh<<endl;
				cout<<"Diem TB: "<<DiemTB<<endl;
		}
};
class LopHoc{
	private:
		char TenLop[32];
		int SoSV;
		SinhVien *DanhSachSV;
	public:
		LopHoc()
		{
			TenLop[32]='a';
			SoSV=1;
			DanhSachSV=NULL;
		}
		~LopHoc(){}
		void TimKiem()
		{
			DanhSachSV=new SinhVien[SoSV+1];
			SinhVien x;
			int m=0;
			cout<<"Nhap thong tin sinh vien can tim kiem: "<<endl;
			x.Nhap();
/*			for(int i=0; i<SoSV; i++)
				if (x.MaSV==DanhSachSV[i].MaSV && x.NamSinh==DanhSach[i].NamSinh && x.DiemTB==DanhSachSV[i].DiemTB && strcmp(x.TenSV,DanhSachSV[i].TenSV)==0)
					m++;*/
			if(m==0) cout<<"Khong co sinh vien nay"<<endl;
			else cout<<"Sinh Vien nay co trong lop"<<endl;
		}
};
main()
{
}
