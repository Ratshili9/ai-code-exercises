import unittest
from merge_sort import merge_sort

class TestMergeSort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_element(self):
        self.assertEqual(merge_sort([42]), [42])

    def test_already_sorted(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        # Triggers left-dominant drain loop
        self.assertEqual(merge_sort([9, 7, 5, 3, 1]), [1, 3, 5, 7, 9])

    def test_duplicates(self):
        self.assertEqual(merge_sort([5, 1, 5, 3, 1]), [1, 1, 3, 5, 5])

    def test_negative_numbers(self):
        self.assertEqual(merge_sort([-3, -10, 5, 0, -1]), [-10, -3, -1, 0, 5])

if __name__ == "__main__":
    unittest.main()
