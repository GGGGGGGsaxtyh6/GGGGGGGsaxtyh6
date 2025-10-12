#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE 100

long get_random() {
	return rand() % BUFSIZE;
}

long increment(long in) {
	return in + 1;
}

int main() {
	long ans = get_random();
	ans = increment(ans);
	printf("The number is: %ld\n", ans);
	return 0;
}
