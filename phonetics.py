# coding=utf-8
import json
import random


class Phonetics(object):
    filename = 'example.json'
    phonemes = {}
    exceptions = []
    words = []

    def __init__(self, file=None):
        self.phonemes = {}
        self.exceptions = []
        if file:
            self.filename = file
            self.load()

    def load(self):
        with open(self.filename) as infile:
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

    """parsing sound changes rule with the notation X>Y/Z, where X is a set of source phonemes
    Y - a set of resulting phonemes, Z - a positional condition (optional)"""
    @staticmethod
    def parse_phonetic_rule_notation(inline):
        rule = inline.split('>')
        if len(rule) != 2:
            return []

        source = rule[0].split(',')
        final = rule[1].split('/')

        result = final[0].split(',')
        rule = []
        if len(final) > 2:
            return []
        elif len(final) == 2:
            pos_conf = final[1].split('_')
            if len(pos_conf) != 2:
                return []
            pos_conf[0] = pos_conf[0].split('#')
            pos_conf[1] = pos_conf[1].split('#')

            if (len(pos_conf[0]) == 2) and len(pos_conf[0][0]) > 0:
                return []
            elif len(pos_conf[0]) == 2:
                rule.append(True)
                rule.append(pos_conf[0][1])
            else:
                rule.append(False)
                rule.append(pos_conf[0][0])

            if (len(pos_conf[1]) == 2) and len(pos_conf[1][1]) > 0:
                return []

            rule.append(pos_conf[1][0])
            if len(pos_conf[1]) == 2:
                rule.append(True)
            else:
                rule.append(False)

        final = []
        if len(source) > len(result):
            for i in range(len(result)-1, len(source)-1):
                result.append("")
        elif len(source) < len(result):
            for i in range(len(source)-1, len(result)-1):
                source.append("")

        final.append(source)
        final.append(result)
        if len(rule) > 0:
            final.append(rule)

        return final

    """ check if phonemic sequence follow condition"""
    def is_sequence_match_pattern(self, rule, word, pos, seq):
        begin = rule[0]
        end = rule[3]
        begin_phonemic_class = rule[1] or ('#' if begin else '?')
        end_phonemic_class = rule[2] or ('#' if end else '?')

        word_substr = word[pos-1:pos+len(seq)+1]
        sequence = begin_phonemic_class + seq + end_phonemic_class

        return self.is_sequences_match(word_substr, sequence)

    """check if two phonemic sequences matching"""
    def is_sequences_match(self, seq1, seq2):
        if len(seq1) != len(seq2):
            return False

        for i in range(0, len(seq1)):
            if seq1[i] == seq2[i]:
                pass
            elif seq1[i].isupper() and seq1[i] in self.phonemes and seq2[i] in self.phonemes.get(seq1[i]):
                pass
            elif seq2[i].isupper() and seq2[i] in self.phonemes and seq1[i] in self.phonemes.get(seq2[i]):
                pass
            elif seq1[i] == '?' or seq2[i] == '?':
                pass
            else:
                return False

        return True

    """apply sound change rule to a word"""
    def proceed_phonetic_change(self, word, change):
        law = Phonetics.parse_phonetic_rule_notation(change)
        chars_from = law[0]
        chars_to = law[1]
        rules = law[2]

        res_word = '#'+word+'#'
        # для каждого из сочетания заменяемых звуков
        for i in range(0, len(chars_from)):
            # делаем цикл по всему слову
            for j in range(0, len(res_word)-len(chars_from[i])+1):
                src_seq = res_word[j:len(chars_from[i])+j]

                if self.is_sequence_match_pattern(rules, res_word, j, src_seq):
                    res_seq = Phonetics.set_clear_sequence(src_seq, chars_from[i], chars_to[i])
                    res_word = res_word[:j] + res_seq + res_word[len(src_seq)+j:]
                    break

        return res_word.strip('#')

    """set certain characters of wildcards in resulting sequence"""
    @staticmethod
    def set_clear_sequence(src_seq, chars_from, chars_to):
        res = chars_to
        for i in range(0, len(chars_from)):
            if chars_from[i].isupper():
                if res.find(chars_from[i]) != -1:
                    res = res.replace(chars_from[i], src_seq[i])
        return res
