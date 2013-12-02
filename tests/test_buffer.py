import unittest
from yammy.translator import YammyInputBuffer


class TestYammyInputBuffer(unittest.TestCase):

    def test_iteration(self):
        for l in YammyInputBuffer(['test']):
            self.assertEqual(l, 'test')
