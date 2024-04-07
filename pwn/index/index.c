#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

typedef char Message[100];

Message MESSAGES[3] = {"Are ya winnin', son?", "Good luck getting the flag!", "You got this!"};

char* get_message(unsigned long i) {
    Message* ret = &MESSAGES[i];
    Message* start = &MESSAGES[0];
    Message* end = &MESSAGES[2];
    if (ret < start || end < ret) {
        puts("That's not allowed!");
        exit(0);
    }
    return ret;
}

unsigned long get() {
    unsigned long i = 0;
    scanf("%lu", &i);
    return i;
}

void win() {
    asm("andq $-16, %rsp");
    char buf[64];
    FILE* f = fopen("flag.txt", "r");
    fgets(buf, sizeof(buf), f);
    puts(buf);
}

void vuln() {
    while (1) {
        puts("\n1. Edit a message");
        puts("2. Read a message");
        puts("3. Exit\n");
        unsigned long choice = get();
        if (choice == 1) {
            puts("Enter an index to edit (0-2):");
            char* ptr = get_message(get());
            puts("Enter your new message:");
            memset(ptr, 0, 100);
            read(STDIN_FILENO, ptr, 99);
        }  else if (choice == 2) {
            puts("Enter an index to read (0-2):");
            Message tmp;
            strcpy(tmp, get_message(get()));
            puts(tmp);
        } else {
            break;
        }
    }
}

int main() {
    init();
    vuln();
}
