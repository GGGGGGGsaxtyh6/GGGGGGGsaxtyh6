#include <stdio.h>

typedef struct {
  char a[10];
  char b[10];
  char c[10];
  char flag[5];
} object;

int main() {
    printf("sizeof(object) = %lu\n", sizeof(object));
    printf("offset of flag = %lu\n", __builtin_offsetof(object, flag));
    return 0;
}
