
#include <stdio.h>

void f(int a, double d, char c, signed s) {}

int main()
{
    int a = 1 + 1;
    unsigned u = 1 + 1;
    double d = 1 + 2 + 6.666666;

    ((1 == 1) && (1 < 2));

    f(a, d, 'c', 4);

	return 0;
}