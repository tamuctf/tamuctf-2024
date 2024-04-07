#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <stdio.h>

int lucky_numbers[777]; 

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    volatile int seed;
    int fd = open("/dev/urandom", O_RDONLY);
    read(fd, (char*)&seed, sizeof(seed));
    read(fd, (char*)&lucky_numbers, sizeof(lucky_numbers));
    srand(seed);
    seed = 0;

    close(fd);
}

int main() {
    init();

    puts("I'll give you a flag if you can guess the next 7 calls to rand(). As a benevolent level creator, I'll give you 21 free lucky numbers! Take your pick 0-777:");
    for (int i = 0; i < 21; ++i) {
        unsigned long pick = 0;
        scanf("%lu", &pick);
        printf("Here's lucky number #%d: %d\n", i + 1, lucky_numbers[pick]);
    }

    int all_correct = 1;

    for (int i = 0; i < 7; ++i) {
        int guess = 0;
        printf("Enter guess #%d:\n", i + 1);
        scanf("%d", &guess);
        all_correct &= guess == rand();
    }

    if (all_correct) {
        char buf[64];
        FILE* f = fopen("flag.txt", "r");
        fgets(buf, sizeof(buf), f);
        puts(buf);
    } else {
        puts("That's not correct :(");
    }
}
