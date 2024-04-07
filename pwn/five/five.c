#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

void init() {
    // ignore
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

int main() {
    init();
    char* input = mmap(main + 0x10000, 0x1000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    read(0, input, 5);
    puts("glhf!");
    ((void (*)())(input))();
}
