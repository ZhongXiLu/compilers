
#include <stdio.h>

int main()
{
    int a;

    while (a < 10) {
        if (a == 8) {
            break;
        } else {
            a = a + 1;
        }
    }

    if (a != 0) {
        printf("%d", a);
    }

    return 0;
}