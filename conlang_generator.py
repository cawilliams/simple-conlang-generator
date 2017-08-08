#!/usr/bin/python3
import os
import sys
import json
import random

words = []
phonemes = {}
exceptions = []
filename = 'example.json'

running = True

def generate_words(sample, phonemes, num=10):
    global words
    gen = True
    r = random.random()
    word = ""
    i = 0
    while i < int(num):
        for j in range(0, len(sample)):
            if sample[j] == '(':
                gen = (random.randint(0,1) == 0)
            elif sample[j] == ')':
                gen = True
            else:
                for n, phtype in enumerate(phonemes.keys()):
                    if gen and phtype == sample[j]:
                        k = random.choice(phonemes[phtype])
                        word += k
        if (not word in words) and (not isExceptional(word)):
            words.append(word)

        i += 1
        word = ""

def isExceptional(word):
    global exceptions
    for i in range(0, len(exceptions)):
        if exceptions[i] in word:
            return True
    return False



def command_exec(cmd):
    global words, phonemes, filename, exceptions
    params = cmd.split()
    if params == []:
        print("Phonemes:\n")
        print(phonemes)
        print("Forbidden clusters:\n")
        print(exceptions)

    elif params[0] == "exit":
        running = False

    elif params[0] == "gen":
        words = []
        if len(params) == 2:
            generate_words(params[1], phonemes)
        elif len(params) == 3:
            generate_words(params[1], phonemes, params[2])
        else:
            print("! Error, can't generate words")

        for i,w in enumerate(words):
            if i==0 or i%10:
                print(w+" ", end='')
            else:
                print(w+"\n", end='')
        print()

    elif params[0] == "set":
        #pars = 0
        
        if params[1] == "ph" and len(params) == 4:
            phonemes[params[2]] = params[3]
        elif params[1] == "ex" and len(params) > 2:
            i = 2
            while i < len(params):
                if not params[i] in exceptions:
                    exceptions.append(params[i])
                else:
                    exceptions.remove(params[i])
                i += 1
        else:
            print("! Error, can't execute a command")

        

    elif params[0] == "savewords":
        if len(params) == 2:
            sw = open(params[1]+".txt", 'w')
            for i,w in enumerate(words):
                if i==0 or i%10:
                    sw.write(w+' ')
                else:
                    sw.write(w+'\n')

    elif params[0] == "reset":
        phonemes = {}
        exceptions = []

    elif params[0] == "save":
        if (len(params) > 2):
            if params[1] == "ph":
                filename = params[2]
                with open(filename, 'w') as outfile_ph:
                    json.dump(phonemes, outfile_ph)
            elif params[1] == "ex":
                filename = params[2]
                with open(filename, 'w') as outfile_ex:
                    json.dump(exceptions, outfile_ex)
        else:
            print("! Error, can't save a file")

    elif params[0] == "load":
        if (len(params)>2):
            if params[1] == "ph":
                filename = params[2]
                with open(filename, 'r') as data_file_ph:    
                    phonemes = json.load(data_file_ph)
            elif params[1] == "ex":
                filename = params[2]
                with open(filename, 'r') as data_file_ex:    
                    exceptions = json.load(data_file_ex)
        else:
            print("! Error, can't load a file")

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
    


print("This is a word generator for your conlang :3\nType 'help' for additional info\n")
while running:
    command = input(">> ")
    command_exec(command)
