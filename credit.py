card_num = input("Please provide your card number: ")

amex_len = 15
mastercard_len = 16
visa_lens = [13, 16]

amex_start = ["34", "37"]
mc_start = ["51", "52", "53", "54", "55"]
visa_start = "4"


def get_card_products_list(card):
    products = []
    for number in range(-2, -len(card) - 1, -2):
        products.append(2*int(card[number]))

    return products


def sum_products_list(prod_list):
    final_sum = 0
    for prod in prod_list:
        if prod >= 10:
            prod_integers = str(prod)

            for integer in prod_integers:
                final_sum += int(integer)
        else:
            final_sum += prod

    return final_sum


def complete_final_sum(prod_sum, card):
    print(f"Completing final sum. Starting with: {prod_sum}")
    final_sum = prod_sum
    for number in range(-1, -len(card) - 1, -2):
        # print(f"Index: {number}. Card num: {int(card[number])}")
        final_sum += int(card[number])

    return str(final_sum)


def get_card_checksum(card):
    products = get_card_products_list(card)
    # print(f"Products: {products}")
    sum_of_even_prods = sum_products_list(products)
    # print(f"Sum of evens: {sum_of_even_prods}")
    result = complete_final_sum(sum_of_even_prods, card)

    # print(result)

    if int(result[-1]) == 0:
        return True
    else:
        return False


def determine_bank(card):
    checksum = get_card_checksum(card)
    if card.startswith("4") and checksum and len(card) in visa_lens:
        print("VISA")
    elif card[0:2] in mc_start and checksum and len(card) == mastercard_len:
        print("MASTERCARD")
    elif card[0:2] in amex_start and checksum and len(card) == amex_len:
        print("AMEX")
    else:
        # print(f"Card start: {card[0:2]}. Checksum: {checksum}. Length: {len(card)}")
        print("INVALID")

determine_bank(card_num)


# MC1: 5555555555554444
# MC2: 5105105105105100
