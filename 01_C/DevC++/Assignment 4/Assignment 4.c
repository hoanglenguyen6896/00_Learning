/*
Write a program for managing the students which contains below info:
• Student’s name
• Student’s ID
• Math score
Requirements:
1. Using linked list for management.
2. Implement the function to add, remove,
find a student info from list by student’s ID
3. Implement a console menu for using feature add, remove, find
4. Follow to coding convention as other assignments.
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

struct LinkedList
{
	char cIDStudent[100];
	char cNameStudent[20];
	float fMathScore;
    struct LinkedList *next;
 };
typedef struct LinkedList *node;

/* Create a new node */
node nCreateNode(char *cID, char *cName, float fScore)
{
    node nTemp = NULL;
    nTemp = (node)malloc(sizeof(struct LinkedList));
    nTemp->next = NULL;
    strcpy(nTemp->cIDStudent, cID);
    strcpy(nTemp->cNameStudent, cName);
    nTemp->fMathScore = fScore;
    return nTemp;
}

/* Add a note to tail of List */
node nAddNodeTail(node nHead, char *cID, char *cName, float fScore)
{
	node nTemp = NULL;
	node nNextNode = NULL;
	nTemp = nCreateNode(cID, cName, fScore);
	/* If list is empty, add to list */
	if(nHead == NULL) nHead = nTemp;

	else
	{
		nNextNode = nHead;
		while(nNextNode->next != NULL)
		{
			nNextNode = nNextNode->next;
		}
		nNextNode->next = nTemp;
	}
	return nHead;
}

/* Add an student to List */
node nAddAnInfo(node nHead)
{
	char cStdName[100];
	char cStdID[20];
	float fMScore = 0.0f;
	
	printf("-----------\n");
	printf("Add a student to List...\n");
	printf("Enter student information...\n");
	
	printf("\tStudent ID: ");
	fflush(stdin);
	gets(cStdID);

	printf("\tStudent Name: ");
	fflush(stdin);
	gets(cStdName);

	printf("\tStudent's Math Score: ");
	scanf("%f", &fMScore);
	printf("-----------\n");
	nHead = nAddNodeTail(nHead, cStdID, cStdName, fMScore);
	return nHead;
}

/* Create a Linked List */
node nCreateList()
{
	node nHead = NULL;
	uint8_t iNoNode = 0u;
	uint8_t i = 0u;
	char cStdName[100];
	char cStdID[20];
	float fMScore = 0.0f;
	do
	{
		printf("Enter the number of Student: ");
		scanf("%d", &iNoNode);
		
	}
	while(iNoNode <= 0u);
	for(i=0u; i<iNoNode; i++)
	{
		printf("Enter student information...\n");
		printf("\tStudent ID: ");
		fflush(stdin);
		gets(cStdID);
		
		printf("\tStudent Name: ");
		fflush(stdin);
		gets(cStdName);
		
		printf("\tStudent's Math Score: ");
		scanf("%f", &fMScore);
		
		nHead = nAddNodeTail(nHead, cStdID, cStdName, fMScore);
	}
	return nHead;
}


/* Print Linked list data */
void vPrintLinked(node nHead)
{
	uint8_t i = 0;
	node nTemp = NULL;
	for(nTemp = nHead; nTemp != NULL; nTemp = nTemp->next)
	{
		i++;
		printf("Student %d Information: \n", i);
		printf("\tStudent ID: ");
		puts(nTemp->cIDStudent);
		
		printf("\tStudent Name: ");
		puts(nTemp->cNameStudent);
		
		printf("\tStudent's Math Score: %f\n\n", nTemp->fMathScore);
	}
}

main() {
	uint8_t iReq = 0;
	node nHead = nCreateList();
	vPrintLinked(nHead);
 	printf("------------- Student Management -------------\n");
	printf("\t1. Add a student to lits\n");
	printf("\t2. Remove a student from lits\n");
	printf("\t3. Find a student in lits\n");
	printf("\t4. Exit\n");
	
	nHead = nAddAnInfo(nHead);
	
	vPrintLinked(nHead);
	return 0;
}
