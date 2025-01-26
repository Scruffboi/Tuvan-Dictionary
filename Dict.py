from docx import Document
import sys
import re


# Gets text into a lowercase comma-separated word list without punctuation
# And without russian
def preprocess(input):
    # line = 1
    wordlist = []
    doc = Document(input)
    paragraphs = doc.paragraphs
    for paragraph in paragraphs:

        # Here it should skip over paragraphs whose line number has been seen already
        # or whatever strategy for skipping the russian parts

        # text = paragraph.text
        # lower = text.lower()
        # nopunc = re.sub(r'[^\w\s-]', '', lower)
        # wordlist.extend(nopunc.split())

    return wordlist

def add_to_dict(dictionary, text):
    for word in text:
        if word in dictionary.keys():
            dictionary[word] = dictionary.get(word) + 1
        else:
            dictionary[word] = 1

# Processes each file one at a time
def main(argv):
    dictionary = {}
    for i in range(1, len(argv)):
        processedText = preprocess(argv[i])
        add_to_dict(dict, processedText)

if __name__ == "__main__":
    main(sys.argv)