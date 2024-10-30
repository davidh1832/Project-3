import unittest


# Function to test
def add(a: int, b: int) -> int:
    """
    This function adds two integers.
    """
    return a+b

# Class for the unit tests.
class TestAddition(unittest.TestCase):
    
    # Testing the add function with specific test cases.
    def test_add(self):
        self.assertEqual(add(10, 20), 30)

# Run all the tests
if __name__ == "__main__":
    unittest.main()