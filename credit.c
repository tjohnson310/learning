#include <stdio.h>
#include <cs50.h>


int main(void)
{
    int mod_cc_number = 0;
    int odds = 0;
    int evens = 0;
    int even_digits = 0;
    int counter = 1;
    int new_digit = 0;
    int sum = 0;
    long cc_number = get_long("Number: ");

    while (cc_number > 0)
    {
        mod_cc_number = cc_number % 10;
        cc_number = cc_number / 10;

        if (counter % 2 == 0)
        {
            even_digits = (mod_cc_number)*2;
            if (even_digits > 9)
            {
                while (even_digits > 0)
                {
                    new_digit = even_digits % 10;
                    evens = evens + new_digit;
                    even_digits = even_digits / 10;
                }
            } else
            {
                evens = evens + even_digits;
            }
        } else
        {
            odds = odds + (mod_cc_number);
        }
        counter++;
    }

    sum = evens + odds;
    if (sum % 10 == 0)
    {
        if (mod_cc_number == 3)
        {
            printf("AMERICAN EXPRESS\n");
        } else if (mod_cc_number == 4)
        {
            printf("VISA\n");
        } else if (mod_cc_number == 5)
        {
            printf("MASTERCARD\n");
        } else
        {
            printf("INVALID\n");
        }
    } else
    {
        printf("INVALID\n");
    }

}
