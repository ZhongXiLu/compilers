
#include <stdio.h>

double f() { return 1.0; }

int main()
{
    int a;

    a = 1;
    a = 1 + 1;
    a = a + a;

    1 == 1 || 1 != 1;
    1 <= 1 && 1 >= 1;
    5*((a - 1)/10);

    double array[3] = {1.0, 2.0, 3.0};

    array[0] + 1.0;
    f() + 1.0;
    (array[2] - 1.0) / (1.0 + f());

	return 0;
}