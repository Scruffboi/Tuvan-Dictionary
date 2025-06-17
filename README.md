This project takes all the words from 3 given Tuvan Mansucripts, and runs segmentation on them, as well as translation of each word. 
The final product is in the form of a CSV, and is located in "tuvan_table_new.csv"

Below I will explain what each class/file does in this project:

Dict.py: 
Scans the 3 manuscripts, (via reading the Tesseract OCR output), and creates a dictionary of unique words, and the lines they appear on.
The output of this is located in "tuvan_dict.csv"

segment.py:
Segments all of the unique words, and finds the translation of both the roots and their morphemes. This class also compiles all of the data collected so far into one CSV, tuvan_table_new.csv

Tuvan Morphemes.txt:
A list of many Tuvan morphemes, (which are all suffixes), and their definitions.
