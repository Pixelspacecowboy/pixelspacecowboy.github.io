import unittest
from student_score_sorter_enhanced import merge_sort, binary_search # type: ignore

# Define a test case class for the Student Score Sorter functions
class TestScoreSorter(unittest.TestCase):

    def setUp(self):
        """
        This method runs before each test.
        It sets up a sample list of students with their scores.
        We also sort the list using merge_sort so we can test binary_search on it.
        """
        self.students = [
            ("Alice", 91),
            ("Bob", 88),
            ("Charlie", 93),
            ("Diana", 85),
            ("Evan", 88)
        ]
        # Sort once and reuse for binary search tests
        self.sorted_students = merge_sort(self.students)

    def test_merge_sort_sorted_order(self):
        """
        Test that merge_sort correctly sorts the list of student tuples by score.
        We extract the scores and confirm they match Python’s built-in sorted() result.
        """
        scores = [score for _, score in self.sorted_students]
        self.assertEqual(scores, sorted(scores))

    def test_binary_search_found(self):
        """
        Test that binary_search returns a result when the target score is present.
        We're looking for the score 88, which exists twice in the dataset.
        We assert the result is not None and the score is correct.
        """
        result = binary_search(self.sorted_students, 88)
        self.assertIsNotNone(result)  # Make sure something is returned
        self.assertIn(result[1], [88])  # Make sure it's one of the valid matches

    def test_binary_search_not_found(self):
        """
        Test that binary_search returns None when the score isn't in the dataset.
        We use a value (100) that doesn't exist in the list to validate the fail case.
        """
        result = binary_search(self.sorted_students, 100)
        self.assertIsNone(result)  # Nothing should be returned

# This allows us to run the tests if we execute this file directly
if __name__ == '__main__':
    unittest.main()

