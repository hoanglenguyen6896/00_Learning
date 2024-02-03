/*
viet 1 function kiem tra mot chuoi ky tu xem chuoi do co the dung lam password duoc khong voi yeu cau thoa man 3 trong cac dieu kien sau
 co it nhat 1 ky tu chu thuong a z
 co it nhat 1 ky tu chu hoa A Z
 co it nhat 1 ky tu so 0 9
 co ky tu dac biet !@#$%^&*-+
va phai
 co toi thieu 8 ky tu !@#$%^&*-+
*/

#include <stdio.h>
#include <string.h>
#include <stdint.h>
uint8_t iCheckPassword(char *password)
{
	/*
	0. When password have atleast 8 character, conditionFlag'll be assigned by 1;
	1. If password have atleast 1 lowercase then assign 1 to lowerCaseFlag;
	2. if password have atleast 1 upercase then assign 1 to upperCaseFlag;
	3. if password have atleast 1 number then assign 1 to numberFlag;
	4. if password have atleast 1 special character from !@#$%^&*-+ then assign 1 to specialCharFlag;
	====> To sastify condition 0 and 3 in 4 conditions from (1-4), conditionFlag must have the smallest sum is 3;
	*/
	uint8_t lowerCaseFlag = 0;
	uint8_t stopLowerCase = 0;
	uint8_t upperCaseFlag = 0;
	uint8_t stopUpperCase = 0;
	uint8_t numberFlag = 0;
	uint8_t stopNumberCase = 0;
	char specialChar[] = {'!','@','#','$','%','^','&','*','-','+'};
	uint8_t specialCharFlag = 0;
	uint8_t stopSpecialChar = 0;
	uint8_t passIndex = 0;
	uint8_t tempIndex = 0;
	if(strlen(password) < 8) return 8;
	else
	{
		for(passIndex = 0; passIndex < strlen(password); passIndex++)
		{
			if('a' <= password[passIndex] && password[passIndex] <= 'z')
			{
				lowerCaseFlag = 1;
				stopLowerCase = 1;
			}
			else if('A' <= password[passIndex] && password[passIndex] <= 'Z')
			{
				upperCaseFlag = 1;
				stopUpperCase = 1;
			}
			else if('0' <= password[passIndex] && password[passIndex] <= '9')
			{
				numberFlag = 1;
				stopNumberCase = 1;
			}
			else
			{
				uint8_t isValidChar = 0;
				for(tempIndex = 0; tempIndex < 10; tempIndex++)
				{
					if(password[passIndex] == specialChar[tempIndex])
					{
						specialCharFlag = 1;
						stopSpecialChar = 1;
						isValidChar ++;
					}
				}
				if(isValidChar == 0) return 10;
			}
		}
	}
	return (lowerCaseFlag + upperCaseFlag + numberFlag + specialCharFlag);
}

main()
{
	char password[100];
	uint8_t passwordValid = 0;
	do{
		printf("Nhap mat khau (Nhap 'e' de thoat): ");
		fflush(stdin);
		gets(password);
		passwordValid = iCheckPassword(password);
		if(passwordValid == 8) printf("-----> Mat khau ban nhap khong hop le (So ky tu it hon 8).\n");
		else if(passwordValid == 10) printf("-----> Mat khau ban nhap khong hop le (Chua ky tu dac biet khong hop le).\n");
		else if(passwordValid < 3) printf("-----> Mat khau ban nhap khong dat du 3/4 dieu kien\n");
		else printf("-----> Mat khau ban nhap hop le.\n");
		printf("\n");
	}while(password[0] != 'e');
	return 0;
}
