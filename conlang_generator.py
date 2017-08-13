#!/usr/bin/python3
# coding=utf-8
from phonetics import Phonetics

running = True


def command_exec(phonetics, cmd):
    params = cmd.split()
    if not params:
        print("Phonemes:")
        print(phonetics.phonemes)
        print("Forbidden clusters:")
        print(phonetics.exceptions)

    elif params[0] == "exit":
        return False, phonetics

    elif params[0] == "gen":
        words = []
        if len(params) == 2:
            words = phonetics.generate_words(params[1])
        elif len(params) == 3:
            words = phonetics.generate_words(params[1], params[2])
        else:
            print("! Error, can't generate words")

        for i, w in enumerate(words):
            if i == 0 or i % 10:
                print(w+" ", end='')
            else:
                print(w+"\n", end='')
        print()

    elif params[0] == "set":

        if params[1] == "ph" and len(params) == 4:
            phonetics.phonemes[params[2]] = params[3]

        elif params[1] == "ex" and len(params) > 2:
            for ex in params[2:]:
                if ex not in phonetics.exceptions:
                    phonetics.exceptions.append(ex)
                else:
                    phonetics.exceptions.remove(ex)
        else:
            print("! Error, can't execute a command")

    elif params[0] == "savewords":
        if len(params) == 2:
            sw = open(params[1]+".txt", 'w')
            for i, w in enumerate(phonetics.words):
                if i == 0 or i % 10:
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
        print("set ex <exception1> [exception2] ... [exceptionN] - add/remove forbidden phonemic sequences;")
        print("reset - reset phonemic invertory;")
        print("load ph <filename> - load phonemic invertory from file;")
        print("load ex <filename> - load forbidden phonemic sequences from file;")
        print("save ph <filename> - save phonemic invertory to file;")
        print("save ex <filename> - save forbidden phonemic sequences to file;")
        print("gen <phonemicPattern> [amountOfWords] - generate words;")
        print("savewords <filename> - save wordlist to file;")
        print("exit - close program")

    return True, phonetics

if __name__ == '__main__':
    print("This is a word generator for your conlang :3\nType 'help' for additional info\n")
    phon = Phonetics()

    while running:
        command = input(">> ")
        running, phon = command_exec(phon, command)
