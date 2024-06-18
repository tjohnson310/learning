import re
import math


text = input("Please provide the text to evaluate: ")

def get_index(text_string):
    letters_num = 0
    word_num = 0
    sentence_num = 0

    words = re.split(r'\W+', text_string)
    sentences = text_string.split(".")

    sentence_num = len(sentences) - 1
    word_num = len(words) - 1

    for word in words:
        current_word_letter_count = len(word)
        letters_num += current_word_letter_count

    average_letters = (letters_num / word_num) * 100
    average_sentences = (sentence_num / word_num) * 100

    index = (0.0588 * average_letters) - (0.296 * average_sentences) - 15.8

    return index


grade = round(get_index(text))

if grade < 1:
    print("Before Grade 1");
elif grade > 16:
    print("Grade 16");
else:
    print("Grade:", grade);

