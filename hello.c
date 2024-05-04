#include <cs50.h>
#include <stdio.h> //header file "standard I/O" (i.e. code, libraries that someone else wrote). Akin to import statements in Python.

int main(void)
{
    string name = get_string("What's your name? ");
    printf("hello, %s!\n", name);
}
