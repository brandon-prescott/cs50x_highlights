#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    float pixel_average = 0;

    // For each row
    for (int i = 0; i < height; i++)
    {
        // For each column
        for (int j = 0; j < width; j++)
        {
            // Take the average RGB value for the current pixel and round to the nearest integer
            pixel_average = roundf((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            // Overwrite the existing RBG values for the pixel with the average
            image[i][j].rgbtBlue = pixel_average;
            image[i][j].rgbtGreen = pixel_average;
            image[i][j].rgbtRed = pixel_average;

        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    // Floats to store the original RGB pixel values
    float original_red = 0;
    float original_green = 0;
    float original_blue = 0;

    // Floats to store the coverted RGB values using the sepia function
    float sepia_red = 0;
    float sepia_green = 0;
    float sepia_blue = 0;

    // For each row
    for (int i = 0; i < height; i++)
    {
        // For each column
        for (int j = 0; j < width; j++)
        {

            // Store the original RGB values for the current pixel
            original_red = image[i][j].rgbtRed;
            original_green = image[i][j].rgbtGreen;
            original_blue = image[i][j].rgbtBlue;

            // Calculate the converted sepia RBG values
            sepia_red = roundf(0.393 * original_red + 0.769 * original_green + 0.189 * original_blue);
            sepia_green = roundf(0.349 * original_red + 0.686 * original_green + 0.168 * original_blue);
            sepia_blue = roundf(0.272 * original_red + 0.534 * original_green + 0.131 * original_blue);

            // If statements to cap the maximum value at 255
            if (sepia_red > 255)
            {
                sepia_red = 255;
            }

            if (sepia_green > 255)
            {
                sepia_green = 255;
            }

            if (sepia_blue > 255)
            {
                sepia_blue = 255;
            }

            // Overwrite the existing RGB values for the current pixel with the sepia conversion
            image[i][j].rgbtRed = sepia_red;
            image[i][j].rgbtGreen = sepia_green;
            image[i][j].rgbtBlue = sepia_blue;

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    // Integers to temporarily store one of the swap values
    int tmp_red = 0;
    int tmp_green = 0;
    int tmp_blue = 0;

    // For each row
    for (int i = 0; i < height; i++)
    {
        // For each column up until the middle pixel (width / 2)
        for (int j = 0; j < width / 2; j++)
        {
            // Store the RGB values for the current pixel in a temporary variable
            tmp_red = image[i][j].rgbtRed;
            tmp_green = image[i][j].rgbtGreen;
            tmp_blue = image[i][j].rgbtBlue;

            // Set the current pixel's RGB values to the mirrored pixel at the opposite end of the row
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;

            // Overwrite the mirrored pixel with the original values stored in the temporary variables
            // This has effectively swapped the two pixels mirrored around the centre of the image
            image[i][width - 1 - j].rgbtRed = tmp_red;
            image[i][width - 1 - j].rgbtGreen = tmp_green;
            image[i][width - 1 - j].rgbtBlue = tmp_blue;

        }
    }

    return;
}

// Blur image using box blur method
// This method looks at the current pixel and overwrites its values with the average of the immediately surrounding pixels
// In most cases, this is the average of a 3x3 matrix
// For the edge and corner pixels, anyting outside of the range is ignored
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    // Array to store a copy of the image data
    RGBTRIPLE copy[height][width];

    // Floats to store the sum of the surrounding pixel data and the total number of active pixels in the calculation
    float active_pixel_count = 0.0;
    float red_total = 0;
    float green_total = 0;
    float blue_total = 0;


    // For each row
    for (int i_copy = 0; i_copy < height; i_copy++)
    {
        // For each column
        for (int j_copy = 0; j_copy < width; j_copy++)
        {
            // Add the data from the image array into the copy array
            copy[i_copy][j_copy] = image[i_copy][j_copy];

        }
    }

    // For each row
    for (int i = 0; i < height; i++)
    {
        // For each column
        for (int j = 0; j < width; j++)
        {
            // Re-initalise each variable
            active_pixel_count = 0.0;
            red_total = 0;
            green_total = 0;
            blue_total = 0;

            // For each row in the box array for the current pixel
            for (int y = i - 1; y <= i + 1; y++)
            {
                // For each column in the box array for the current pixel
                for (int x = j - 1; x <= j + 1; x++)
                {
                    // If statement which checks if the current element in the box array lies outside of the image array
                    if (x < 0 || x >= width || y < 0 || y >= height)
                    {
                        // Ignore this element
                        continue;
                    }
                    else
                    {
                        // Increase the number of active pixels required for the average calculation and sum the RGB values in the box array for the current pixel
                        active_pixel_count += 1;
                        red_total += copy[y][x].rgbtRed;
                        green_total += copy[y][x].rgbtGreen;
                        blue_total += copy[y][x].rgbtBlue;

                    }
                }
            }

            // Overwrite the existing RGB values for the current pixel with the average values of the current box array
            image[i][j].rgbtRed = roundf(red_total / active_pixel_count);
            image[i][j].rgbtGreen = roundf(green_total / active_pixel_count);
            image[i][j].rgbtBlue = roundf(blue_total / active_pixel_count);

        }
    }

    return;
}
