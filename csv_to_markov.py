import sys
import csv
from collections import defaultdict
import markovify
import nltk
import re

# Command line interface:
# python3 csv_to_markov.py groupme_clowns.csv "name"
#
# optionally, specify number of sentences to generate
# python3 csv_to_markov.py groupme_clowns.csv "name" 20
#
# or specify one of the functions: "contains_word", "starts_with", or "ends_with"
# python3 csv_to_markov.py groupme_clowns.csv "name" 20 "ends_with" "some words"

class POSifiedText(markovify.NewlineText):
    def __init__(self, *args, **kwargs):
        reverse = kwargs['reverse']
        kwargs.pop('reverse', None)
        self.reverse = reverse
        markovify.NewlineText.__init__(self, *args, **kwargs)

    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        if self.reverse is True:
            words.reverse()
        return words

    def word_join(self, words):
        clean_words = list(word.split("::")[0] for word in words)
        if self.reverse is True:
            clean_words = reversed(clean_words)
        sentence = " ".join(clean_words)
        return sentence

    def make_sentence(self, *args, **kwargs):
        kwargs['max_overlap_ratio'] = .5
        return super().make_sentence(*args, **kwargs)

def getAuthorId(authorIds, authorNames, arg):
    for (index, name) in enumerate(authorNames):
        if name.startswith(arg):
            return authorIds[index]

def readCsv():
    authorIds = []
    authorId = None
    messages = []

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        messages = []
        for index, row in enumerate(reader):
            if index == 0:
                authorIds = row
            if index == 1:
                authorId = getAuthorId(authorIds, row, sys.argv[2])
            if index > 1 and row[1] == authorId:
                for sentence in row[3].split('.'):
                    messages.append(sentence.strip())

    text = '\n'.join(messages)
    return text


def buildModel(text, reverse, state_size):
    return POSifiedText(text, reverse=reverse, state_size=state_size)






def standard(times):
    model = buildModel(readCsv(), False, 2)

    count = 0
    while(count < times):
        sentence = model.make_sentence()
        if (sentence is not None):
            count = count + 1
            print(sentence)

def contains_word(times, word):
    model = buildModel(readCsv(), False, 2)

    godCount = 0
    while(godCount < times):
        sentence = model.make_sentence()
        if (sentence is not None):
            if word in sentence.lower():
                godCount = godCount + 1
                print(sentence)

def starts_with(times, arg):
    model = buildModel(readCsv(), False, len(arg.split(' ')))
    count = 0

    while(count < times):
        sentence = model.make_sentence_with_start(arg)
        if (sentence is not None):
            count = count + 1
            print(sentence)

def ends_with(times, arg):
    if len(sys.argv) < 4:
        return

    model = buildModel(readCsv(), True, len(arg.split(' ')))
    count = 0

    while(count < times):
        sentence = model.make_sentence_with_start(arg)
        if (sentence is not None):
            count = count + 1
            print(sentence)

times = 20
if len(sys.argv) > 3:
    times = int(sys.argv[3])

command = None
if len(sys.argv) > 4:
    command = sys.argv[4]

if command == "starts_with":
    starts_with(times, sys.argv[5])
elif command == "ends_with":
    ends_with(times, sys.argv[5])
elif command == "contains_word":
    contains_word(times, sys.argv[5])
else:
    standard(times)
