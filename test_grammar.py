import unittest
from main_app import clean_and_check_sentence

class TestSpellSyncGrammar(unittest.TestCase):
    
    def test_possessives_and_homophones(self):
        self.assertEqual(clean_and_check_sentence("every student were asked to present there project"), "every student was asked to present their project")

    def test_verb_forms_and_agreement(self):
        self.assertEqual(clean_and_check_sentence("a small robot which can detects obstacles but it were not working"), "a small robot which can detect obstacles but it was not working")

    def test_uncountable_nouns_and_advice(self):
        self.assertEqual(clean_and_check_sentence("which was a advice we needed"), "which was advice we needed")

    def test_reported_questions(self):
        self.assertEqual(clean_and_check_sentence("one of the judges asked us why does our model produce heat"), "one of the judges asked us why our model was producing heat")

    def test_correct_sentences_remain_unchanged(self):
        correct_sentence = "The exhibition was a great success for all students."
        self.assertEqual(clean_and_check_sentence(correct_sentence), correct_sentence)

if __name__ == '__main__':
    unittest.main()