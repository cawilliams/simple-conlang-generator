#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest
from phonetics import Phonetics

TESTFILE_1 = os.path.join(os.path.dirname(__file__), 'test_conlang.json')


class TestInterpreter(unittest.TestCase):
    """conlang generator interpreter unittest"""
    conlang = None

    ruleBegin = "sk>x/#_"
    ruleEnd = "e,o,a>/_#"
    ruleBefore = "Vl>lV/_C"
    ruleAfter = "k>x/R_"
    ruleMiddleEdge = "ai>ee/#C_C#"
    ruleMiddle = "ai>ia/C_C"

    @classmethod
    def setUpClass(cls):
        """ Setup """
        cls.conlang = Phonetics(TESTFILE_1)

    """test sequences match"""
    def test_sequences_matches_positive(self):
        self.assertTrue(self.conlang.is_sequences_match("k","k"))
        self.assertTrue(self.conlang.is_sequences_match("abc","abc"))
        self.assertTrue(self.conlang.is_sequences_match("ABC","ABC"))

        self.assertTrue(self.conlang.is_sequences_match("k","C"))
        self.assertTrue(self.conlang.is_sequences_match("C","k"))

        self.assertTrue(self.conlang.is_sequences_match("kC","CC"))
        self.assertTrue(self.conlang.is_sequences_match("Ck","CC"))

        self.assertTrue(self.conlang.is_sequences_match("CC", "kC"))
        self.assertTrue(self.conlang.is_sequences_match("CC", "Ck"))

        self.assertTrue(self.conlang.is_sequences_match("kk","CC"))
        self.assertTrue(self.conlang.is_sequences_match("CC","kk"))

    def test_sequences_matches_negative(self):
        self.assertFalse(self.conlang.is_sequences_match("N","k"))
        self.assertFalse(self.conlang.is_sequences_match("k","N"))

        self.assertFalse(self.conlang.is_sequences_match("abc","ABC"))

    """test rule parsing"""
    def test_parse_rule_begin(self):
        res = self.conlang.parse_phonetic_rule_notation(self.ruleBegin)
        self.assertEqual([['sk'], ['x'], [True, '', '', False]], res)

    def test_parse_rule_end(self):
        res = self.conlang.parse_phonetic_rule_notation(self.ruleEnd)
        self.assertEqual([['e', 'o', 'a'], ['', '', ''], [False, '', '', True]], res)

    def test_parse_rule_before(self):
        res = self.conlang.parse_phonetic_rule_notation(self.ruleBefore)
        self.assertEqual([['Vl'], ['lV'], [False, '', 'C', False]], res)

    def test_parse_rule_after(self):
        res = self.conlang.parse_phonetic_rule_notation(self.ruleAfter)
        self.assertEqual([['k'], ['x'], [False, 'R', '', False]], res)

    def test_parse_rule_middle(self):
        res = self.conlang.parse_phonetic_rule_notation(self.ruleMiddle)
        self.assertEqual([['ai'], ['ia'], [False, 'C', 'C', False]], res)

    def test_parse_rule_middle_edge(self):
        res = self.conlang.parse_phonetic_rule_notation(self.ruleMiddleEdge)
        self.assertEqual([['ai'], ['ee'], [True, 'C', 'C', True]], res)

    """test rule applying"""

    """begin"""
    def test_apply_rule_begin(self):
        word = self.conlang.proceed_phonetic_change("skuska", self.ruleBegin)
        self.assertEqual("xuska", word)

    def test_apply_rule_begin_negative(self):
        word = self.conlang.proceed_phonetic_change("askuska", self.ruleBegin)
        self.assertNotEqual("axuska", word)

    """end"""
    def test_apply_rule_end(self):
        word = self.conlang.proceed_phonetic_change("tete", self.ruleEnd)
        self.assertEqual("tet", word)

    def test_apply_rule_end_negative(self):
        word = self.conlang.proceed_phonetic_change("teten", self.ruleEnd)
        self.assertNotEqual("tetn", word)

    """middle"""
    def test_apply_rule_end(self):
        word = self.conlang.proceed_phonetic_change("kait", self.ruleMiddle)
        self.assertEqual("kiat", word)

    def test_apply_rule_end_negative(self):
        word = self.conlang.proceed_phonetic_change("ai", self.ruleMiddle)
        self.assertNotEqual("ia", word)

if __name__ == '__main__':
    unittest.main()
