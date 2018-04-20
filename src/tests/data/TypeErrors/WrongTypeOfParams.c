
#include <stdio.h>

int f(int a, char c, unsigned u) {}

int main()
{
    int a;
    char c;
    unsigned u;
    f(a, u, c); // ERROR

	return 0;
}