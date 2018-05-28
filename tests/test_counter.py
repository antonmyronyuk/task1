import unittest

from counter import count_unique_words as cnt


class TestCounter(unittest.TestCase):

    def test_none_text(self):
        with self.assertRaises(ValueError):
            cnt(None)

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            cnt('')

    def test_spaces_string(self):
        self.assertEqual(cnt('          '), 0)
        self.assertEqual(cnt(' '), 0)

    def test_punctuations_string(self):
        self.assertEqual(cnt(','), 0)
        self.assertEqual(cnt(',.?$'), 0)
        self.assertEqual(cnt('   ?   '), 0)
        self.assertEqual(cnt('  ,.  ?  **  / '), 0)

    def test_alpha_string(self):
        self.assertEqual(cnt('Word'), 1)
        self.assertEqual(cnt('Some word'), 2)
        self.assertEqual(cnt('How do you do?'), 3)
        self.assertEqual(cnt('word Word   WORD ? wOrD'), 1)
        self.assertEqual(cnt('     Hello ,.&   from..........test     '), 3)

    def test_digits_string(self):
        """Numbers are also words"""
        self.assertEqual(cnt('121212'), 1)
        self.assertEqual(cnt('1 2 1 2 1 2'), 2)
        self.assertEqual(cnt('1 2 3 4 5'), 5)
        self.assertEqual(cnt('?????????111-222-333     '), 3)
        self.assertEqual(cnt('2pac 4ever'), 2)

    def test_underscore_string(self):
        """Underscore '_' is a word too"""
        self.assertEqual(cnt('_'), 1)
        self.assertEqual(cnt('   _____   '), 1)
        self.assertEqual(cnt('lol_kek__'), 1)
        self.assertEqual(cnt('__private ,,,'), 1)
        self.assertEqual(cnt('for _ in words'), 4)
        self.assertEqual(cnt('   ,. 1_2_3 ,, 1_2_3_4,,1_2_3'), 2)

    def test_unicode(self):
        """Some unicode characters are also words"""
        self.assertEqual(cnt('отакої'), 1)
        self.assertEqual(cnt('Що це має бути?'), 4)
        self.assertEqual(cnt('顔文    字'), 2)
        # smiles != words
        self.assertEqual(cnt('🎅 🍜  ⏱ ㋡ 🌲'), 0)
