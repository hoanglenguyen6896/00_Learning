import unittest
import chap06_cap

class TestCap(unittest.TestCase):
    """
    """
    def test_one_word(self):
        text = 'python'
        result = chap06_cap.cap_text(text)
        self.assertEqual(result, 'Python')

    def test_multi_words(self):
        text = 'monty python'
        result = chap06_cap.cap_text(text)
        self.assertEqual(result, 'Monty Python')

if __name__ == '__main__':
    unittest.main()
