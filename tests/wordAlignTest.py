#!/usr/bin/python

import unittest

from Modules.wordAlign import initialize, backtrace


class WordAlignTest(unittest.TestCase):
    def test_should_return_valid_matrixes(self):
        _reference_words = 2
        _hypothesis_words = 2
        align_matrix, backtrace_matrix = initialize(_reference_words, _hypothesis_words)
        self.assertEqual(align_matrix, [[0, 1, 2], [1, 0, 0], [2, 0, 0]])
        self.assertEqual(backtrace_matrix, [[2, 1, 1], [2, 0, 0], [2, 0, 0]])

    def test_should_return_backtrace(self):
        refs = ["REF1", "REF2"]
        hyps = ["HYP1", "HYP2"]
        backtrace_matrix = [[2, 1, 1], [2, 0, 0], [2, 0, 0]]

        expected = {'alignment':[('REF1', 'HYP1'), ('REF2', 'HYP2')],'Ins':0,'Del':0,'Subs':2}
        actual = backtrace(refs, hyps, "", backtrace_matrix)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
