from docx import Document
import sys
import re
import csv


# Gets text into a lowercase, no punctuation, comma-separated word list containing tuples of word and line number
def preprocess(input):
    # wordlist will contain tuples of word and line number
    wordlist = []
    line_num = 1
    doc = Document(input)
    paragraphs = doc.paragraphs
    for paragraph in paragraphs:

        # Here it should skip over paragraphs whose line number has been seen already
        # or whatever strategy for skipping the russian parts

        text = paragraph.text
        lower = text.lower()
        nopunc = re.sub(r'[^\w\s-]|[\d+]|i', '', lower)
        for line in nopunc.splitlines():
            for word in line.split():
                # format as tuple
                formatted = (word, line_num)
                wordlist.append(formatted)
            line_num += 1
    return wordlist


# Dictionary of words to list of line numbers the word appears
def add_to_dict(dictionary, text):
    for word, line_num in text:
        if word in dictionary.keys():
            dictionary[word].append(line_num)
        else:
            dictionary[word] = [line_num]


# Writes dictionary to output csv file
def output_to_csv(dictionary):
    with open("tuvan_dict.csv", mode="w", newline="", encoding="utf-8") as file:
        column_name = ['Word', 'Line Numbers']
        writer = csv.DictWriter(file, fieldnames=column_name)
        writer.writeheader()
        for word, lines in dictionary.items():
            writer.writerow({"Word": word, "Line Numbers": ", ".join(map(str, lines))})


# Processes each file one at a time
def main(argv):
    dictionary = dict()
    for i in range(1, len(argv)):
        processed_text = preprocess(argv[i])
        add_to_dict(dictionary, processed_text)
    output_to_csv(dictionary)

if __name__ == "__main__":
    main(sys.argv)