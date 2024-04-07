#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/conf.h>

unsigned long auth_len = 0x123456789;
unsigned long dec_len = 0x987654321;
unsigned char func_key[16] = "0123456789ABCDEF";

bool check_debug() {
  if(ptrace(PTRACE_TRACEME, 0, NULL, NULL) != 0) {
    fprintf(stderr, "Debugger detected!\n");
    ptrace(PTRACE_KILL, 0, NULL, NULL);
    exit(0);
  }
  return false;
}

void decrypt_func(unsigned char* enc, int len) {
  for(uint64_t i = 0; i < len; i++) {
    enc[i] = enc[i] ^ func_key[i % 16];
  }
}

void __attribute__((section(".dec"))) decrypt_password(const unsigned char* in, unsigned char* out) {
  unsigned char key[16] = {0xb4, 0x9f, 0xe8, 0xf5, 0x90, 0x97, 0xb9, 0x0b, 0x5a, 0xb9, 0xbb, 0xce, 0xba, 0x9f, 0xb8, 0x81};
  unsigned char iv[16]  = {0x6c, 0x5e, 0x03, 0x99, 0xde, 0x6f, 0xd3, 0x2e, 0x78, 0x3d, 0xb8, 0x11, 0xd1, 0x4c, 0x1d, 0xde};
  unsigned int xor[4] = {0xde, 0xad, 0xbe, 0xef};

  for(int i = 0; i < 16; i++) {
    key[i] = key[i] ^ xor[i % 4];
    iv[i] = iv[i] ^ xor[i % 4];
  }

  int outsz;

  EVP_CIPHER_CTX *ctx;

  if(!(ctx = EVP_CIPHER_CTX_new())) {
    ptrace(PTRACE_KILL, 0, NULL, NULL);
    ERR_print_errors_fp(stderr);
    abort();
  }

  if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv)) {
    ptrace(PTRACE_KILL, 0, NULL, NULL);
    ERR_print_errors_fp(stderr);
    abort();
  }

  if(1 != EVP_DecryptUpdate(ctx, out, &outsz, in, 0x20)) {
    ptrace(PTRACE_KILL, 0, NULL, NULL);
    ERR_print_errors_fp(stderr);
    abort();
  }

  if(1 != EVP_DecryptFinal_ex(ctx, out + outsz, &outsz)) {
    ptrace(PTRACE_KILL, 0, NULL, NULL);
    ERR_print_errors_fp(stderr);
    abort();
  }
}

void __attribute__((section(".auth"))) auth() {
  unsigned char encpass[0x20] = {0x92, 0xea, 0x0f, 0x8b, 0x77, 0xdf, 0x97, 0xe7, 0x91, 0xd2, 0xeb, 0xf7, 0x0c, 0xbd, 0x07, 0x8d, 0xcc, 0x7d, 0xcf, 0x2a, 0x5d, 0x2c, 0x25, 0xed, 0x95, 0xee, 0x7d, 0xf5, 0xaf, 0x85, 0x26, 0x23};

  unsigned char decpass[0x10];
  char in[0x10];

  printf("Input password: ");
  read(0, in, 0x10);
  
  mprotect((void*)((unsigned long)decrypt_password & 0xfffffffffffff000), (uint64_t)(dec_len + ((unsigned long)auth - ((unsigned long)auth & 0xfffffffffffff000))), PROT_READ | PROT_WRITE | PROT_EXEC);
  decrypt_func((unsigned char*)decrypt_password, dec_len);
  mprotect((void*)((unsigned long)decrypt_password & 0xfffffffffffff000), (uint64_t)(dec_len + ((unsigned long)auth - ((unsigned long)auth & 0xfffffffffffff000))), PROT_READ | PROT_EXEC);
  decrypt_password((unsigned char*)encpass, (unsigned char*)decpass);

  if(memcmp(decpass, in, 0x10) != 0) {
    puts("Incorrect password");
    return;
  }

  FILE* f = fopen("flag.txt", "r");
  if(f == NULL) {
    puts("No flag found, try your password on the server!");
    return;
  }
  
  unsigned char flag[36];
  fgets((char*)flag, 36, f);
  printf("%s", flag);
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  prctl(PR_SET_DUMPABLE, 0);

  if(!check_debug()) {
    mprotect((void*)((unsigned long)auth & 0xfffffffffffff000), (uint64_t)(auth_len + ((unsigned long)auth - ((unsigned long)auth & 0xfffffffffffff000))), PROT_READ | PROT_WRITE | PROT_EXEC);
    decrypt_func((unsigned char*)auth, auth_len);
    mprotect((void*)((unsigned long)auth & 0xfffffffffffff000), (uint64_t)(auth_len + ((unsigned long)auth - ((unsigned long)auth & 0xfffffffffffff000))), PROT_READ | PROT_EXEC); 
    auth();
    ptrace(PTRACE_KILL, 0, NULL, NULL);
  }
}
