#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    int new_pixel_color;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            new_pixel_color = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            // Update pixel values
            image[i][j].rgbtBlue = new_pixel_color;
            image[i][j].rgbtGreen = new_pixel_color;
            image[i][j].rgbtRed = new_pixel_color;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed;
    int sepiaGreen;
    int sepiaBlue;
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);

            if (sepiaBlue > 255)
                sepiaBlue = 255;

            if (sepiaGreen > 255)
                sepiaGreen = 255;

            if (sepiaRed > 255)
                sepiaRed = 255;

            // Update pixel with sepia values
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
            int avg_red;
            int avg_blue;
            int avg_green;

            // Middle pixels
            if ((i - 1) >= 0 && (i + 1) < height && (j + 1) < width && (j - 1) >= 0)
            {
                avg_red = round((image[i-1][j-1].rgbtRed +  image[i-1][j].rgbtRed +  image[i-1][j+1].rgbtRed + \
                                image[i][j-1].rgbtRed +  image[i][j].rgbtRed +  image[i][j+1].rgbtRed + \
                                image[i+1][j-1].rgbtRed + image[i+1][j].rgbtRed +  image[i+1][j+1].rgbtRed) / 9.0);

                avg_green = round((image[i-1][j-1].rgbtGreen + image[i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen + \
                                    image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen + \
                                    image[i+1][j-1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen) / 9.0);

                avg_blue = round((image[i-1][j-1].rgbtBlue + image[i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue + \
                                    image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue + \
                                    image[i+1][j-1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue) / 9.0);

                copy[i][j].rgbtBlue = avg_blue;
                copy[i][j].rgbtGreen = avg_green;
                copy[i][j].rgbtRed = avg_red;
            }
            // Top Edge
            else if (i == 0 && (j - 1) >= 0 && (j + 1) < width)
            {
                avg_red = round((image[i][j-1].rgbtRed +  image[i][j].rgbtRed +  image[i][j+1].rgbtRed + \
                                image[i+1][j-1].rgbtRed + image[i+1][j].rgbtRed +  image[i+1][j+1].rgbtRed) / 6.0);

                avg_green = round((image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen + \
                                    image[i+1][j-1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen) / 6.0);

                avg_blue = round((image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue + \
                                    image[i+1][j-1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue) / 6.0);

                copy[i][j].rgbtBlue = avg_blue;
                copy[i][j].rgbtGreen = avg_green;
                copy[i][j].rgbtRed = avg_red;
            }
            // Bottom edge
            else if (i == (height - 1) && (j - 1) >= 0 && (j + 1) < width)
            {
                avg_red = round((image[i-1][j-1].rgbtRed +  image[i-1][j].rgbtRed +  image[i-1][j+1].rgbtRed + \
                                image[i][j-1].rgbtRed +  image[i][j].rgbtRed +  image[i][j+1].rgbtRed) / 6.0);

                avg_green = round((image[i-1][j-1].rgbtGreen + image[i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen + \
                                    image[i][j-1].rgbtGreen + image[i][j].rgbtGreen + image[i][j+1].rgbtGreen) / 6.0);

                avg_blue = round((image[i-1][j-1].rgbtBlue + image[i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue + \
                                    image[i][j-1].rgbtBlue + image[i][j].rgbtBlue + image[i][j+1].rgbtBlue) / 6.0);

                copy[i][j].rgbtBlue = avg_blue;
                copy[i][j].rgbtGreen = avg_green;
                copy[i][j].rgbtRed = avg_red;
            }
            // Top Left Corner
            else if (i == 0 && j == 0 && (j + 1) < width)
            {
                avg_red = round((image[i][j].rgbtRed +  image[i][j+1].rgbtRed + image[i+1][j].rgbtRed + image[i+1][j+1].rgbtRed) / 4.0);

                avg_green = round((image[i][j].rgbtGreen +  image[i][j+1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen) / 4.0);

                avg_blue = round((image[i][j].rgbtBlue +  image[i][j+1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue) / 4.0);

                copy[i][j].rgbtBlue = avg_blue;
                copy[i][j].rgbtGreen = avg_green;
                copy[i][j].rgbtRed = avg_red;
            }
            // Top Right Corner
            else if (i == 0 && j == (width - 1))
            {
                avg_red = round((image[i][j].rgbtRed +  image[i][j-1].rgbtRed + image[i+1][j].rgbtRed + image[i+1][j-1].rgbtRed) / 4.0);

                avg_green = round((image[i][j].rgbtGreen +  image[i][j-1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j-1].rgbtGreen) / 4.0);

                avg_blue = round((image[i][j].rgbtBlue +  image[i][j-1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j-1].rgbtBlue) / 4.0);

                copy[i][j].rgbtBlue = avg_blue;
                copy[i][j].rgbtGreen = avg_green;
                copy[i][j].rgbtRed = avg_red;
            }
            // Bottom Left Corner
            else if (i == (height - 1) && j == 0 && (j + 1) < width)
            {
                avg_red = round((image[i][j].rgbtRed +  image[i-1][j+1].rgbtRed + image[i-1][j].rgbtRed + image[i][j+1].rgbtRed) / 4.0);

                avg_green = round((image[i][j].rgbtGreen +  image[i-1][j+1].rgbtGreen + image[i-1][j].rgbtGreen + image[i][j+1].rgbtGreen) / 4.0);

                avg_blue = round((image[i][j].rgbtBlue +  image[i-1][j+1].rgbtBlue + image[i-1][j].rgbtBlue + image[i][j+1].rgbtBlue) / 4.0);

                copy[i][j].rgbtBlue = avg_blue;
                copy[i][j].rgbtGreen = avg_green;
                copy[i][j].rgbtRed = avg_red;
            }
            // Bottom Right Corner
            else if (i == (height - 1) && j == (width + 1))
            {
                avg_red = round((image[i][j].rgbtRed +  image[i-1][j].rgbtRed + image[i-1][j-1].rgbtRed + image[i][j-1].rgbtRed) / 4.0);

                avg_green = round((image[i][j].rgbtGreen +  image[i-1][j].rgbtGreen + image[i-1][j-1].rgbtGreen + image[i][j-1].rgbtGreen) / 4.0);

                avg_blue = round((image[i][j].rgbtBlue +  image[i-1][j].rgbtBlue + image[i-1][j-1].rgbtBlue + image[i][j-1].rgbtBlue) / 4.0);

                copy[i][j].rgbtBlue = avg_blue;
                copy[i][j].rgbtGreen = avg_green;
                copy[i][j].rgbtRed = avg_red;
            }
        }
        for (int k = 0; k < height; k++)
        {
            for (int l = 0; l < width; l++)
            {
                image[k][l] = copy[k][l];
            }
        }
    }
    return;
}
