import csv
import sys
import json
import re


# gets list of words (from the manuscript) from the given csv file (in this case "tuvan_dict.csv")
def listify(file):
    # convert csv to data structure (list of dicts)
    output = list()
    with open(file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        output = list(reader)

    # extract list of words and line_nums from data struc of csv
    # note its the form of a tuple
    words = [(item['Word'], item['Line Numbers']) for item in output]

    return words


# Collects all the morphemes from the given csv (in this case "Tuvan Morphemes.txt")
def get_morphemes(file):
    output = dict()
    with open(file, newline='', encoding="utf-8") as f:
        for line in f:
            words = line.split()
            if words[0] == '$' or words[0][1] == ',':
                continue
            morpheme = words[0][:-1]
            gloss = ''
            for i in range(1, len(words)):
                gloss += words[i] + ' '
            output[morpheme] = gloss
    return output


# Scrapes the json file for all dictionary entries and definition
def get_roots(file):
    gloss_dict = dict()
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in range(len(data)):
            word = data[i]['word']
            gloss = data[i]['translation']

            # check that dictionary entry is just ONE word
            # some entries have more than one variation, so we check if any are one word long (what we want)
            # compound words with a dash (-) don't count
            # we also don't want to include parentheses or brackets in dictionary entries
            variations = re.split(r', |\(|\[', word)
            for variation in variations:
                if len(variation.split()) == 1 and '-' not in variation and ')' not in variation and ']' not in variation:
                    gloss_dict[variation] = gloss

        return gloss_dict


# Segments words and formats all information that will be needed for the CSV
def segment(words, morphemes, roots):
    count = 0

    # This is the format we will need the output csv to be in
    # It's a list of dicts, with the keys as the headers and values as what will goes in that column
    # Root, Gloss, Morphemes
    format = list()
    # for roots and morphemes, longer is preferred
    # this is why I sorted them like this
    roots_sorted = sorted(roots.keys(), key=len, reverse=True)
    morphemes_sorted = sorted(morphemes.keys(), key=len, reverse=True)
    morpheme_pattern = r"(" + r"|".join(map(re.escape, morphemes_sorted)) + r")$"
    root_pattern = r"^(" + r"|".join(map(re.escape, roots_sorted)) + r")"

    for word, line_nums in words:

        row_dict = dict()
        # start index determines where suffix segmentation should start (but its actually where it ends since its backwards)
        # end_index marks what part of the word is currently being segmented, we are segmenting backwards
        start_index = 0
        end_index = len(word)
        # format variables
        root = ''
        gloss = ''
        suffixes = list()

        # check for root at start at word, if so make boundary for suffix segmentation
        match = re.search(root_pattern, word)
        if match:
            root = match.group()
            gloss = roots[root]
            start_index = len(root)

        # stop once we have segmented the whole word
        while end_index != start_index:
            match = re.search(morpheme_pattern, word[start_index:end_index])
            suffix = ''

            # check for longest morpheme that matches end of word
            if match:
                suffix = match.group()
                suffixes.append(suffix + ' (' + morphemes[suffix].strip() + ')')
            else:
                # if no match is found, keep searching word, if we didn't have this line would run forever
                end_index -= 1

            end_index = end_index - len(suffix)

        row_dict['Word'] = word
        row_dict['Root'] = root
        row_dict['Gloss'] = gloss
        suffixes.reverse()
        row_dict['Morphemes'] = suffixes
        row_dict['Line Numbers'] = line_nums
        format.append(row_dict)

        count += 1
        print(count)

    return format


# Creates final CSV with all information
def output_to_csv(format):
    with open("tuvan_table_new.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Word", "Root", "Gloss", "Morphemes", "Line Numbers"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(format)


def main(argv):
    list_of_words = listify(argv[1])
    morpheme_dict = get_morphemes(argv[2])
    root_dict = get_roots(argv[3])

    format = segment(list_of_words, morpheme_dict, root_dict)
    output_to_csv(format)


if __name__ == "__main__":
    main(sys.argv)
