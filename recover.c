#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc == 2)
    {
        char *raw_file = argv[argc - 1];

    }
    else if (argc < 2 || argc > 2)
    {
        printf("Usage: ./recover raw_file\n");
        return 1;
    }

    FILE *images = fopen(raw_file, "r");
    if (images == NULL)
    {
        printf("Could not open %s.\n", raw_file);
        return 1;
    }
}
