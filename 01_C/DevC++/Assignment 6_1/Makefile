#Compiler: gcc
CC = gcc

#Macros
TARGET = main

#Execute
build: $(TARGET).o ass6.o menu.o
	$(CC) -o $(TARGET).exe $(TARGET).o ass6.o menu.o

$(TARGET).o: $(TARGET).c
	$(CC) -c $(TARGET).c
menu.o: menu.c
	$(CC) -c menu.c
ass6.o: ass6.c
	$(CC) -c ass6.c
clean:
	$(RM) $(TARGET).exe