import csv
import sys


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 dna.py [dna_csv_file] [sequence_txt_file]")
        raise Exception

    strs = []
    humans = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        strs = reader.fieldnames
        strs = strs[1::]
        for row in reader:
            humans.append(row)

    # print(f"STRs: {strs}")
    # print(f"DNA Data: {humans}")

    with open(sys.argv[2], "r") as file:
        sequence_data = file.read()

    # print(f"Sequence data: {sequence_data}")

    # TODO: Find longest match of each STR in DNA sequence
    result_dict = {}
    for _str in strs:
        result_dict[_str] = longest_match(sequence_data, _str)

    # print(fr"Result: {result_dict}")

    match = []
    for human in humans:
        current_human = human["name"]

        for _str in strs:
            if result_dict[_str] == int(human[_str]):
                match.append(True)

        if len(match) == len(strs):
            print(current_human)
            break

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
