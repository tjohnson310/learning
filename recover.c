#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

typedef struct
{
    BYTE jfFirst;
    BYTE jfSecond;
    BYTE jfThird;
    BYTE jfFourth;
} __attribute__((__packed__))
JPEGFILEHEADER;

int main(int argc, char *argv[])
{
    char *raw_file;
    if (argc == 2)
    {
        raw_file = argv[argc - 1];

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

    uint8_t buffer[512];
    bool jpeg_working = false;
    int file_count = 0;
    char filename[9];
    sprintf(filename, "%03i.jpg", file_count);
    FILE *img = fopen(filename, "w");

    while (fread(&buffer, 1, 512, images) == 512)
    {
        // Ensure raw_file is the start or end of a jpeg
        if (buffer[0] == 0xff || buffer[1] == 0xd8 || buffer[2] == 0xff ||
            (buffer[3] & 0xf0) == 0xe0)
        {
            // First block kicks off writing the first jpeg.
            if (!jpeg_working)
            {
                fwrite(&buffer, 512, 1, img);
                jpeg_working = true;
            }
            // Second block closes the last jpeg and kicks off creation of the next.
            else if (jpeg_working)
            {
                fclose(img);
                file_count += 1;

                char new_file[9];

                sprintf(new_file, "%03i.jpg", file_count);
                img = fopen(new_file, "w");
                fwrite(&buffer, 512, 1, img);
            }
        }
        else if (jpeg_working)
        {
            fwrite(&buffer, 512, 1, img);
        }
    }
    fclose(images);
}
