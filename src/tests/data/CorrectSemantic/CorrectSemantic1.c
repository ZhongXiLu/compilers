
#include <stdio.h>

void f(int a) {}

int main()
{
    int a;
    a;
    {
        int d;
        f(a);
        {
            a;
            d;
        }
    }

    int array[100];

    array[0];
    array[100];

	return 0;
}