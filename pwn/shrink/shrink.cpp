#include <cstdio>
#include <unistd.h>
#include <string>

void upkeep() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
}

void win() {
    char flag[64] = {0};
    FILE* f = fopen("flag.txt", "r");
    if (!f) {
        perror("missing flag.txt");
        return;
    }
    fgets(flag, 64, f);
    puts(flag);
}

struct Username {
    std::string buf = "this_is_a_default_username";
    size_t len = 26;
    void print() {
        puts(buf.data());
    }
    void change() {
        puts("Enter your new name: ");
        int i = read(0, (void*)buf.data(), len);
        if (i > 0) {
            buf.resize(i);
            buf.shrink_to_fit();
        }
    }
    void add_exclamation() {
        buf += "!";
        len += 1;
    }
};

void vuln() {
    Username username;
    int choice = 0;
    bool going = true;

    while (going) {
        puts("Select an option:");
        puts("1. Print username");
        puts("2. Change username");
        puts("3. Make username more exciting");
        puts("4. Exit");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                username.print();
                break;
            case 2:
                username.change();
                break;
            case 3:
                username.add_exclamation();
                break;
            default:
                going = false;
                break;
        }

    }
}

int main() {
	upkeep();
    vuln();
}
