#include <stdio.h>
#include <stdlib.h>

int upkeep() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
}

void print_maps() {
    FILE* f = fopen("/proc/self/maps", "r");
    char buf[0x1000];
    size_t n = fread(buf, 1, sizeof(buf), f);
    fwrite(buf, 1, n, stdout);
    fflush(stdout);
    fclose(f);
}

void vuln() {
    char buf[128];
    printf("buf is at %p\n", buf);
    gets(buf);
}

int main() {
    upkeep(); 
    puts("Look, the stack isn't RWX!");
    print_maps();
    vuln();
}

