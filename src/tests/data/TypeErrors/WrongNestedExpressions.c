
#include <stdio.h>

char f() {}

int main()
{
    double array[2] = {1, 2};
    int a = 1 - ((12 + array[0]) / 100) * f();  // ERROR
	return 0;
}