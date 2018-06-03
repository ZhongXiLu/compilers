
#include <stdio.h>

int fibonacci(int x) {
    if (x == 1 || x == 2) {
        return 1;
    } else {
        return fibonacci(x - 1) + fibonacci(x - 2);
    }
}

int main()
{
    int i;

    printf("Please enter an integer: ");
    scanf("%i", i);
    printf("The %i-th fibonacci number is %i", i, fibonacci(i));

    return 0;
}
