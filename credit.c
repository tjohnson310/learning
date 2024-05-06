#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int mod_cc_number = 0;
    int odds = 0;
    int evens = 0;
    int even_digits = 0;
    int counter = 0;
    int new_digit = 0;
    int sum = 0;
    int starting_two = 0;
    long cc_number = get_long("Number: ");

    while (cc_number > 0)
    {
        counter++;
        mod_cc_number = cc_number % 10;
        cc_number = cc_number / 10;

        if (counter % 2 == 0)
        {
            even_digits = (mod_cc_number) * 2;
            // printf("\nEven digits: %i\n", even_digits);
            if (even_digits > 9)
            {
                while (even_digits > 0)
                {
                    new_digit = even_digits % 10;
                    // printf("New digit: %i\n", new_digit);
                    evens = evens + new_digit;
                    even_digits = even_digits / 10;
                    // printf("%i-%i-%i ", mod_cc_number, counter, evens);
                }
            }
            else
            {
                evens = evens + even_digits;
                // printf("%i-%i-%i ", mod_cc_number, counter, evens);
            }
        }
        else
        {
            odds = odds + (mod_cc_number);
            // printf("%i-%i ", mod_cc_number, odds);
        }

        if (cc_number < 100 && cc_number > 10)
        {
            starting_two = cc_number;
            // printf("\n%i\n", starting_two);
        }
    }

    sum = evens + odds;
    if (sum % 10 == 0)
    {
        printf("%i\n", sum);
        if (mod_cc_number == 3 && counter == 15 && (starting_two == 34 || starting_two == 37))
        {
            printf("AMEX\n");
        }
        else if (mod_cc_number == 4 && (counter == 13 || counter == 16))
        {
            printf("VISA\n");
        }
        else if (mod_cc_number == 5 && counter == 16 && starting_two < 56)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
