#!/usr/bin/python3
import os
import sys
import json
import random

words = []
phonemes = {}
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
        if not word in words:
            words.append(word)
            i += 1
        word = ""

def command_exec(cmd):
    global words, phonemes, filename
    params = cmd.split()
    if params == []:
        print(phonemes)

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
        pars = 0
        if len(params) == 3:
            phonemes[params[1]] = params[2]

        else:
            print("! Error, can't set the phonemes inventory")

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

    elif params[0] == "save":
        if len(params) > 1:
            filename = params[1]
        with open(filename, 'w') as outfile:
            json.dump(phonemes, outfile)

    elif params[0] == "load":
        if len(params) > 1:
            filename = params[1]
        with open(filename, 'r') as data_file:    
            phonemes = json.load(data_file)

    elif params[0] == "help":
        print("set <typeOfPhoneme> <phonemes> - set class of phonemes typed with a single string")
        print("reset' - reset phonemic invertory")
        print("load <filename> - load phonemic invertory from file")
        print("save <filename> - save phonemic invertory to file")
        print("gen <phonemicPattern> [amountOfWords] - generate words")
        print("savewords <filename>' - save wordlist to file")
        print("exit' - close program")


print("This is a word generator for your conlang :3\nType 'help' for additional info\n")
while running:
    command = input(">> ")
    command_exec(command)