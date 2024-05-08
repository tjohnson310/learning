#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

float get_index(string a);

int main(void)
{
    string text = get_string("Text: ");
    float grade = get_index(text);

    grade = round(grade);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade: %i\n", (int) grade);
    }
}

float get_index(string a)
{
    int counter = 0;
    int letters_num = 0;
    int word_num = 0;
    int sentence_num = 0;
    bool prev_char_alpha = false;
    bool prev_char_single_quote = false;
    bool prev_word_contraction = false;
    for (int i = 0, n = strlen(a); i < n; i++)
    {
        if (isalpha(a[i]))
        {
            prev_char_alpha = true;
            letters_num++;
            if (prev_char_single_quote)
            {
                word_num++;
                prev_char_single_quote = false;
                prev_word_contraction = true;
            }
        }
        else if (isspace(a[i]) && prev_char_alpha)
        {
            prev_char_alpha = false;
            if (!prev_word_contraction)
            {
                word_num++;
            }
            else
            {
                prev_word_contraction = false;
            }
        }
        else if (ispunct(a[i]) && prev_char_alpha)
        {
            prev_char_alpha = false;
            if (a[i] != ';' && a[i] != ':' && a[i] != ',' && a[i] != '\'' && a[i] != '-')
            {
                word_num++;
                sentence_num++;
            }
            else if (a[i] == ',')
            {
                word_num++;
            }
            else if (a[i] == '\'')
            {
                prev_char_single_quote = true;
            }
            else if (a[i] == '-')
            {
                word_num++;
            }

        }
    }
    // printf("Letters: %i\n", letters_num);
    // printf("Words: %i\n", word_num);
    // printf("Sentence: %i\n", sentence_num);
    float avg_letters = ((float) letters_num / (float) word_num) * 100;
    float avg_sentences = ((float) sentence_num / (float) word_num) * 100;

    float index = (0.0588 * avg_letters) - (0.296 * avg_sentences) - 15.8;

    return index;
}
