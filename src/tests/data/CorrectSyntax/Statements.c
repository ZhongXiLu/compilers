
#include <stdio.h>

int f() {
    return 1 + 1;
}

int main()
{
    {
        { { { { {} } } } }
    }

    {
        if (1 == 1) {}
        if (1 == 1) {} else {}
    }

    while (1 == 1) {
        if (1 ==1)
            break;
    }

	return 0;
}