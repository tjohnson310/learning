#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int calculate_score(string a);

const string pt_1_letters = "AEILNORSTU";
const string pt_2_letters = "DG";
const string pt_3_letters = "BCMP";
const string pt_4_letters = "FHVWY";
const string pt_5_letters = "K";
const string pt_8_letters = "JX";
const string pt_10_letters = "QZ";

int main(void)
{
    string p1_word = get_string("Player 1: ");
    string p2_word = get_string("Player 2: ");

    int p1_score = calculate_score(p1_word);
    int p2_score = calculate_score(p2_word);

    if (p1_score > p2_score)
    {
        printf("Player 1 wins!\n");
    }
    else if (p2_score > p1_score)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

}


int calculate_score(string a)
{
    int score = 0;
    for (int i = 0, n = strlen(a); i < n; i++)
    {
        int current_letter = toupper(a[i]);
        for (int j = 0, m = strlen(pt_1_letters); j < m; j++)
        {
            if (current_letter == pt_1_letters[j])
            {
                score++;
            }
        }

        for (int j = 0, m = strlen(pt_2_letters); j < m; j++)
        {
            if (current_letter == pt_2_letters[j])
            {
                score = score + 2;
            }
        }

        for (int j = 0, m = strlen(pt_3_letters); j < m; j++)
        {
            if (current_letter == pt_3_letters[j])
            {
                score = score + 3;
            }
        }

        for (int j = 0, m = strlen(pt_4_letters); j < m; j++)
        {
            if (current_letter == pt_4_letters[j])
            {
                score = score + 4;
            }
        }

        for (int j = 0, m = strlen(pt_5_letters); j < m; j++)
        {
            if (current_letter == pt_5_letters[j])
            {
                score = score + 5;
            }
        }

        for (int j = 0, m = strlen(pt_8_letters); j < m; j++)
        {
            if (current_letter == pt_8_letters[j])
            {
                score = score + 8;
            }
        }

        for (int j = 0, m = strlen(pt_10_letters); j < m; j++)
        {
            if (current_letter == pt_10_letters[j])
            {
                score = score + 10;
            }
        }
    }

    return score;
}
