
#include <stdio.h>

void f(int a, double d, char c, signed s) {}

int main()
{
    int a = 1 + 1;
    unsigned u = 1 + a;
    double d = a + u + 6.666666;

    int array[100];
    double dd = array[0] + array[1] + d;

    ((1 == 1) && (1 < 2));

    f(a, d, 'c', 4);

	return 0;
}