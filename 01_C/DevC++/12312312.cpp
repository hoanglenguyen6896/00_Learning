#include<stdio.h>
#include<fcntl.h>
#include<sys/stat.h>
main()
{
	char word[50];
	int i,j;
	char tab[]="\t[";
	char ctab[]="]";
	char br[]="\n";
	while(1)
	{
		gets(word);
		FILE *t;
		t = fopen("teptin","wb");
		fwrite(word,sizeof(word),1,t);
		fwrite(tab,sizeof(tab),1,t);
		fwrite(ctab,sizeof(ctab),1,t);
		fwrite(br,sizeof(br),1,t);
		memset(word, 0, sizeof(word));
		fclose(t);
	}
}

