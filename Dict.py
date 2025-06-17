import sys
import re
import csv


# Gets text into a lowercase, no punctuation, comma-separated word list containing tuples of word and line number
def preprocess(input, manuscript):
    # Lines that have issues and must be hard-coded to fix (overlap lines)
    hanging_lines = {605, 843, 908, 943, 1095, 1130, 1324}
    skip_lines = {938}

    wordlist = []

    # First two lines are title
    line_num = -1
    file = open(input, "r", encoding="utf-8")
    text = file.read()

    for line in text.splitlines():

        # Watch for blank lines
        if line != '':

            lower = line.lower()
            # deleted -
            nopunc = re.sub(r'[^\w\s-]|[\d+]|i', '', lower)

            # Watch for numbers (that got deleted and are now blank lines) and standalone dashes
            if nopunc != '' and nopunc != '-':

                # deals with problem lines
                if line_num - 1 in hanging_lines:
                    hanging_lines.remove(line_num - 1)
                    line_num -= 1
                elif line_num - 1 in skip_lines:
                    skip_lines.remove(line_num - 1)
                    line_num += 1

                for word in re.split(r'[\s-]+', nopunc):
                    # This is a debug statement YOU CAN DELETE THIS
                    if line_num < 20:
                        print(nopunc)
                        print(str(re.split(r'[\s-]+', nopunc)))

                    # Leading whitespaces are counted as words in the above regex so we must not count them
                    if word != '':
                        formatted = (word, line_num, manuscript)
                        wordlist.append(formatted)
                line_num += 1
    file.close()
    return wordlist


# Dictionary of words to list of line numbers the word appears
def add_to_dict(dictionary, text):
    for word, line_num, manuscript in text:
        if word in dictionary.keys():
            dictionary[word].append(str(line_num) + manuscript)
        else:
            dictionary[word] = [str(line_num) + manuscript]


# Writes dictionary to output csv file
def output_to_csv(dictionary):
    with open("tuvan_dict.csv", mode="w", newline="", encoding="utf-8") as file:
        column_name = ['Word', 'Line Numbers']
        writer = csv.DictWriter(file, fieldnames=column_name)
        writer.writeheader()
        for word, lines in dictionary.items():
            writer.writerow({"Word": word, "Line Numbers": ", ".join(map(str, lines))})


def letter_equivalent(x):
    if x == 1: return 'A'
    if x == 2: return 'B'
    else: return 'C'


# Processes each file one at a time
def main(argv):
    dictionary = dict()
    for i in range(1, len(argv)):
        manuscript = letter_equivalent(i)
        processed_text = preprocess(argv[i], manuscript)
        add_to_dict(dictionary, processed_text)
    output_to_csv(dictionary)

if __name__ == "__main__":
    main(sys.argv)