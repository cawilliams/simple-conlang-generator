#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from conlang_generator import command_exec as execute


class TestInterpreter(unittest.TestCase):

    """ conlang generator interpreter unittest """

    def test_exit(self):
        running, phonetics = execute(None, "exit")
        self.assertFalse(running)
        self.assertEqual(phonetics, None)

if __name__ == '__main__':
    unittest.main()
