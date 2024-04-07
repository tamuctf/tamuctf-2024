#include <stdio.h>
#include <unistd.h>
#include <seccomp.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <stdlib.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

char FLAG[64] = "test";
void load_flag() {
    FILE* f = fopen("flag.txt", "r");
    if (!f) {
        puts("no flag found D:");
        return;
    }
    fgets(FLAG, 64, f);
}

int main() {
    init();
    char* rwx = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    load_flag();
    read(STDIN_FILENO, rwx, 0x1000);

    if (fork() > 0) {
        int ret = 0;
        wait(&ret);
        if (ret != 0) {
            puts("something went wrong D:");
        } else {
            puts("adios");
        }
    } else {
        scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
        seccomp_load(ctx);
        ((void (*)())rwx)();
    }
}
