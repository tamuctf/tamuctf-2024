#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
asm(
        "jmp rand\n"
        "jmp srand\n"
        "jmp puts\n"
        "jmp memfrob\n"
        "pop %rcx\n"
        "ret\n"
        "pop %r8\n"
        "ret\n"
        "pop %r9\n"
        "ret\n"
);
char _data_start[1280] = "AAAA";

__attribute__((constructor)) void __do_global_ctors_aux() {
    asm(
        "lea 2(%rip), %rax\n"
        "push %rax\n"
        "ret\n"
    );
    int fd = memfd_create("", 0);
    pwrite(fd, _data_start, 1280, 0);
    dup2(fd, 0);
}
void vuln() {
    char buf[64];
    read(0, buf, 0x69696969);
}
int main() {
    char buf[1280];
    vuln();
}
