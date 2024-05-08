#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void encrypt_message(string message, string key);
int check_key(string key, int letter_count);
string convert_key_to_upper(string key);

const string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

int main(int argc, string argv[])
{
    string encryption_key = argv[1];
    int valid_key = check_key(encryption_key, argc);

    if (valid_key != 0)
    {
        return 1;
    }

    encryption_key = convert_key_to_upper(encryption_key);

    string plaintext = get_string("plaintext: ");
    encrypt_message(plaintext, encryption_key);
}

void encrypt_message(string message, string key)
{
    char current_letter;
    printf("ciphertext: ");
    for (int i = 0, n = strlen(message); i < n; i++)
    {
        current_letter = message[i];

        if (isalpha(current_letter) && isupper(current_letter))
        {
            for (int j = 0, m = strlen(alphabet); j < m; j++)
            {
                if (current_letter == alphabet[j])
                {
                    printf("%c", key[j]);
                }
            }
        }

        if (isalpha(current_letter) && islower(current_letter))
        {
            current_letter = toupper(message[i]);
            for (int j = 0, m = strlen(alphabet); j < m; j++)
            {
                if (current_letter == alphabet[j])
                {
                    printf("%c", tolower(key[j]));
                }
            }
        }

        if (!isalpha(current_letter))
        {
            printf("%c", message[i]);
        }
    }
    printf("\n");
}

int check_key(string key, int letter_count)
{
    char used_letters[26];

    if (letter_count == 1 || letter_count > 2 || strlen(key) < 26)
    {
        printf("Invalid Key: provided an incorrect number of arguments!\n");
        return 1;
    }

    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Invalid Key: contains a character that is not a letter...\n");
            return 1;
        }

        for (int j = 0, m = strlen(used_letters); j < m; j++)
        {
            if (used_letters[j] == key[i])
            {
                printf("Invalid Key: contains a character that is used more than once...\n");
                return 1;
            }
        }
        used_letters[i] = key[i];
    }
    return 0;
}

string convert_key_to_upper(string key)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (islower(key[i]))
        {
            key[i] = toupper(key[i]);
        }
    }
    return key;
}
