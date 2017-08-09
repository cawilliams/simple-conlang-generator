#!/usr/bin/python3
import json
import random

running = True

class Phonetics:
    filename = 'example.json'
    phonemes = {}
    exceptions = []
    words = []

    def __init__(self):
        self.phonemes = {}
        self.exceptions = []

    def load(self):
        with open(self.filename, 'r') as infile:
            data = json.load(infile)
            self.phonemes = data["phonemes"]
            self.exceptions = data["exceptions"]

    def save(self):
        data = {
            "phonemes": self.phonemes,
            "exceptions": self.exceptions
        }
        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile)

    def is_word_exceptional(self, word):
        for ex in self.exceptions:
            if ex in word:
                return True
        return False

    def generate_words(self, sample, num=10):
        self.words = []
        gen = True
        word = ""
        i = 0
        while i < int(num):
            for j in range(0, len(sample)):
                if sample[j] == '(':
                    gen = random.randint(0, 1)
                elif sample[j] == ')':
                    gen = True
                else:
                    if gen:
                        for phtype in self.phonemes.keys():
                            if phtype == sample[j]:
                                k = random.choice(self.phonemes[phtype])
                                word += k

            if not (word in self.words or self.is_word_exceptional(word)):
                self.words.append(word)
                i += 1
            word = ""

        return self.words


def command_exec(phonetics, cmd):
    params = cmd.split()
    if params == []:
        print("Phonemes:")
        print(phonetics.phonemes)
        print("Forbidden clusters:")
        print(phonetics.exceptions)

    elif params[0] == "exit":
        return (False, phonetics)

    elif params[0] == "gen":
        if len(params) == 2:
            words = phonetics.generate_words(params[1])
        elif len(params) == 3:
            words = phonetics.generate_words(params[1], params[2])
        else:
            print("! Error, can't generate words")

        for i, w in enumerate(words):
            if i == 0 or i%10:
                print(w+" ", end='')
            else:
                print(w+"\n", end='')
        print()

    elif params[0] == "set":

        if params[1] == "ph" and len(params) == 4:
            phonetics.phonemes[params[2]] = params[3]

        elif params[1] == "ex" and len(params) > 2:
            for ex in params[2:]:
                if not ex in phonetics.exceptions:
                    phonetics.exceptions.append(ex)
                else:
                    phonetics.exceptions.remove(ex)
        else:
            print("! Error, can't execute a command")

    elif params[0] == "savewords":
        if len(params) == 2:
            sw = open(params[1]+".txt", 'w')
            for i, w in enumerate(phonetics.words):
                if i == 0 or i%10:
                    sw.write(w+' ')
                else:
                    sw.write(w+'\n')

    elif params[0] == "reset":
        phonetics = Phonetics()

    elif params[0] == "save":
        if len(params) > 1:
            phonetics.filename = params[1]
        phonetics.save()

    elif params[0] == "load":
        if len(params) > 1:
            phonetics.filename = params[1]
        phonetics.load()

    elif params[0] == "help":
        print("set ph <typeOfPhoneme> <phonemes> - set class of phonemes typed with a single string;")
        print("set ex <exception1> [exception2] [exception3] ... [exceptionN] - add/remove forbidden phonemic sequences;")
        print("reset - reset phonemic invertory;")
        print("load ph <filename> - load phonemic invertory from file;")
        print("load ex <filename> - load forbidden phonemic sequences from file;")
        print("save ph <filename> - save phonemic invertory to file;")
        print("save ex <filename> - save forbidden phonemic sequences to file;")
        print("gen <phonemicPattern> [amountOfWords] - generate words;")
        print("savewords <filename> - save wordlist to file;")
        print("exit - close program")
    
    return (True, phonetics)


print("This is a word generator for your conlang :3\nType 'help' for additional info\n")
phon = Phonetics()

while running:
    command = input(">> ")
    running, phon = command_exec(phon, command)
